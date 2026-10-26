#!/usr/bin/env python3
"""Pack packages/<id>/ into downloads/<id>.<version>.nupkg without choco/nuget (the build runner is Linux).
Usage: scripts/pack-own.py <env>. A package with envs.json gets that env's values for its $key$ tokens in every file
(openframe-client: the version each env runs, bumped by the openframe-saas-tenant release).

A .nupkg is an OPC zip: the .nuspec at the root, tools/** as declared, plus [Content_Types].xml and _rels/.rels.
Records the result in catalog.json (reason "own") so CATALOG.md covers our packages too.
"""
import hashlib
import json
import re
import sys
import time
import uuid
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGES = ROOT / "packages"
DOWNLOADS = ROOT / "downloads"
CATALOG = ROOT / "catalog.json"

CONTENT_TYPES = """<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml" />
  <Default Extension="psmdcp" ContentType="application/vnd.openxmlformats-package.core-properties+xml" />
  <Default Extension="nuspec" ContentType="application/octet" />
  <Default Extension="ps1" ContentType="application/octet" />
  <Default Extension="md" ContentType="application/octet" />
  <Default Extension="txt" ContentType="application/octet" />
</Types>
"""
RELS = """<?xml version="1.0" encoding="utf-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Type="http://schemas.microsoft.com/packaging/2010/07/manifest" Target="/{nuspec}" Id="R1" />
</Relationships>
"""


def pack(pkg_dir: Path, env: str):
    envs = pkg_dir / "envs.json"
    tokens = json.loads(envs.read_text())[env] if envs.exists() else {}

    def read(f: Path) -> bytes:
        data = f.read_bytes()
        for k, v in tokens.items():
            data = data.replace(f"${k}$".encode(), v.encode())
        return data

    nuspec = next(pkg_dir.glob("*.nuspec"))
    root = ET.fromstring(read(nuspec))
    ns = {"n": root.tag.split("}")[0].strip("{")}
    md = root.find("n:metadata", ns)
    text = lambda tag: (md.findtext(f"n:{tag}", default="", namespaces=ns) or "").strip()
    pkg_id, version = text("id"), text("version")
    out = DOWNLOADS / f"{pkg_id}.{version}.nupkg"
    DOWNLOADS.mkdir(exist_ok=True)
    for old in DOWNLOADS.glob(f"{pkg_id}.[0-9]*.nupkg"):  # another env's version
        old.unlink()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(nuspec.name, read(nuspec))
        for f in sorted((pkg_dir / "tools").rglob("*")):
            if f.is_file():
                z.writestr(f"tools/{f.relative_to(pkg_dir / 'tools').as_posix()}", read(f))
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS.format(nuspec=nuspec.name))
    data = out.read_bytes()
    install = pkg_dir / "tools" / "chocolateyInstall.ps1"
    script = read(install).decode("utf-8-sig") if install.exists() else ""
    deps = [{"id": d.attrib["id"], "range": d.attrib.get("version", "")} for d in root.iterfind(".//n:dependency", ns)]
    return {
        "id": pkg_id, "version": version, "reason": "own", "file": out.name,
        "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
        "community": {"download_url": "", "package_hash_algorithm": "", "package_hash": "", "published": ""},
        "license_url": text("licenseUrl"), "project_url": text("projectUrl"), "authors": text("authors"),
        "dependencies": deps, "has_install_script": bool(script),
        "vendor_urls": sorted(set(re.findall(r"https?://[^\s'\"<>)`]+", script))),
        "vendor_checksums": {}, "embeds_binary": False,
    }


def main():
    env = sys.argv[1]
    records = [pack(d, env) for d in sorted(PACKAGES.iterdir()) if d.is_dir() and any(d.glob("*.nuspec"))]
    catalog = json.loads(CATALOG.read_text()) if CATALOG.exists() else {"source": "", "generated": "", "packages": []}
    own_ids = {r["id"].lower() for r in records}
    catalog["packages"] = [p for p in catalog["packages"] if p["id"].lower() not in own_ids] + records
    catalog["packages"].sort(key=lambda r: r["id"].lower())
    catalog["generated"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    CATALOG.write_text(json.dumps(catalog, indent=2))
    for r in records:
        print(f"packed {r['file']} ({r['size_bytes']} B)")


if __name__ == "__main__":
    main()
