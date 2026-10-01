#!/usr/bin/env python3
"""Mirror curated Chocolatey packages (wrapper .nupkg only) from community.chocolatey.org.

Reads packages.yaml, resolves the dependency closure declared in each .nuspec, downloads every
.nupkg into downloads/, and writes catalog.json with provenance (source URL, hash, size,
dependencies, vendor download URLs + checksums extracted from tools/chocolateyInstall.ps1).
No installers are downloaded: the feed stays link-only.
"""
import hashlib
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOWNLOADS = ROOT / "downloads"
CATALOG = ROOT / "catalog.json"

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
    "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
}
UA = "openframe-chocolatey-packages-sync/0.1 (+https://flamingo.cx)"


def read_packages_yaml(path: Path):
    """Minimal reader for the flat packages.yaml layout (no PyYAML dependency on the runner)."""
    source, pkgs, cur = None, [], None
    for raw in path.read_text().splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue
        if line.startswith("source:"):
            source = line.split(":", 1)[1].strip()
        elif line.strip().startswith("- id:"):
            cur = {"id": line.split(":", 1)[1].strip(), "version": "latest"}
            pkgs.append(cur)
        elif cur and line.strip().startswith("version:"):
            cur["version"] = line.split(":", 1)[1].strip()
    return source, pkgs


def get(url: str, accept="application/atom+xml", retries=4) -> bytes:
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < retries - 1:
                time.sleep(5 * (attempt + 1))  # community feed rate-limits aggressively
                continue
            raise


def prop(entry, name):
    el = entry.find(f"m:properties/d:{name}", NS)
    return (el.text or "").strip() if el is not None else ""


def find_versions(source: str, pkg_id: str):
    """All approved, non-prerelease versions of a package id, newest published first."""
    url = f"{source}FindPackagesById()?id='{pkg_id}'&$orderby=Published%20desc"
    entries = []
    while url:
        root = ET.fromstring(get(url))
        for e in root.findall("a:entry", NS):
            if prop(e, "IsApproved") == "true" and prop(e, "IsPrerelease") != "true":
                entries.append({
                    "version": prop(e, "Version"),
                    "published": prop(e, "Published"),
                    "package_hash": prop(e, "PackageHash"),
                    "package_hash_algorithm": prop(e, "PackageHashAlgorithm"),
                    "package_size": int(prop(e, "PackageSize") or 0),
                    "license_url": prop(e, "LicenseUrl"),
                    "project_url": prop(e, "ProjectUrl"),
                    "dependencies": prop(e, "Dependencies"),
                    "download_url": e.find("a:content", NS).attrib.get("src", ""),
                })
        nxt = root.find("a:link[@rel='next']", NS)
        url = nxt.attrib["href"] if nxt is not None else None
    return entries


def pick(entries, wanted: str):
    if wanted == "latest":
        return entries[0]
    for e in entries:
        if e["version"] == wanted:
            return e
    raise SystemExit(f"version {wanted} not found")


def parse_dependencies(spec: str):
    """Chocolatey OData format: 'id:range:framework|id:range:'. '[1.2.3]' pins, '1.2.3' is a minimum."""
    deps = []
    for part in filter(None, spec.split("|")):
        bits = part.split(":")
        dep_id, rng = bits[0], (bits[1] if len(bits) > 1 else "")
        deps.append({"id": dep_id, "range": rng})
    return deps


def range_to_version(rng: str):
    m = re.fullmatch(r"\[([^,\]]+)\]", rng or "")
    return m.group(1) if m else "latest"


def nuspec_meta(nupkg: bytes):
    """Read id/version/license/dependencies from the .nuspec inside the package."""
    with zipfile.ZipFile(io.BytesIO(nupkg)) as z:
        names = z.namelist()
        spec_name = next(n for n in names if n.endswith(".nuspec") and "/" not in n)
        root = ET.fromstring(z.read(spec_name))
        ns = {"n": root.tag.split("}")[0].strip("{")}
        md = root.find("n:metadata", ns)
        text = lambda tag: (md.findtext(f"n:{tag}", default="", namespaces=ns) or "").strip()
        deps = [
            {"id": d.attrib["id"], "range": d.attrib.get("version", "")}
            for d in root.iterfind(".//n:dependency", ns)
        ]
        install = next((n for n in names if n.lower() == "tools/chocolateyinstall.ps1"), None)
        script = z.read(install).decode("utf-8", "replace") if install else ""
        return {
            "id": text("id"), "version": text("version"), "title": text("title"),
            "license_url": text("licenseUrl"), "project_url": text("projectUrl"),
            "authors": text("authors"), "dependencies": deps, "files": names,
        }, script


def vendor_links(script: str):
    """Pull the vendor download URLs and checksums out of chocolateyInstall.ps1 (best effort)."""
    urls = sorted(set(re.findall(r"https?://[^\s'\"<>)]+", script)))
    checksums = {}
    for key in ("checksum", "checksum64", "checksumType", "checksumType64"):
        m = re.search(rf"(?i)\b{key}\s*=\s*['\"]([^'\"]+)['\"]", script)
        if m:
            checksums[key] = m.group(1)
    embedded = bool(re.search(r"(?i)Install-ChocolateyInstallPackage|\$toolsDir.*\.(exe|msi|zip)", script))
    return urls, checksums, embedded


def main():
    source, wanted = read_packages_yaml(ROOT / "packages.yaml")
    DOWNLOADS.mkdir(exist_ok=True)
    queue = [(p["id"], p["version"], "curated") for p in wanted]
    done, catalog = {}, []
    while queue:
        pkg_id, version, reason = queue.pop(0)
        key = pkg_id.lower()
        if key in done:
            continue
        print(f"[{reason}] {pkg_id} {version}", file=sys.stderr)
        entry = pick(find_versions(source, pkg_id), version)
        data = get(entry["download_url"], accept="application/octet-stream")
        meta, script = nuspec_meta(data)
        fname = f"{meta['id']}.{meta['version']}.nupkg"
        (DOWNLOADS / fname).write_bytes(data)
        sha256 = hashlib.sha256(data).hexdigest()
        urls, checksums, embedded = vendor_links(script)
        record = {
            "id": meta["id"], "version": meta["version"], "reason": reason,
            "file": fname, "size_bytes": len(data), "sha256": sha256,
            "community": {
                "download_url": entry["download_url"],
                "package_hash_algorithm": entry["package_hash_algorithm"],
                "package_hash": entry["package_hash"],
                "published": entry["published"],
            },
            "license_url": meta["license_url"], "project_url": meta["project_url"],
            "authors": meta["authors"],
            "dependencies": meta["dependencies"],
            "has_install_script": bool(script),
            "vendor_urls": urls, "vendor_checksums": checksums,
            "embeds_binary": embedded,
        }
        catalog.append(record)
        done[key] = record
        for d in meta["dependencies"]:
            queue.append((d["id"], range_to_version(d["range"]), f"dependency of {meta['id']}"))
        time.sleep(1)  # be polite to the community feed
    catalog.sort(key=lambda r: r["id"].lower())
    CATALOG.write_text(json.dumps({"source": source, "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "packages": catalog}, indent=2))
    print(f"{len(catalog)} packages → {DOWNLOADS}, catalog → {CATALOG}", file=sys.stderr)


if __name__ == "__main__":
    main()
