#!/usr/bin/env python3
"""Render CATALOG.md from catalog.json (written by sync-community.py)."""
import json
import zipfile
from pathlib import Path

BINARY_EXT = (".exe", ".msi", ".msu", ".msp", ".zip", ".7z", ".nupkg", ".dll", ".cab")

ROOT = Path(__file__).resolve().parent.parent
c = json.loads((ROOT / "catalog.json").read_text())
pk = c["packages"]

def mb(n): return f"{n/1024/1024:.1f} MB" if n >= 1024 * 1024 else f"{n/1024:.0f} KB"

def embedded_files(fname):
    """Binary payload shipped inside the .nupkg itself (what makes a package NOT link-only)."""
    with zipfile.ZipFile(ROOT / "downloads" / fname) as z:
        return [i.filename for i in z.infolist() if i.filename.lower().endswith(BINARY_EXT)]

for p in pk:
    p["embedded_files"] = embedded_files(p["file"])
    p["embeds_binary"] = bool(p["embedded_files"])

out = []
out.append("# Feed catalog\n")
out.append(f"Source: `{c['source']}` · generated {c['generated']} · {len(pk)} packages · "
           f"{mb(sum(p['size_bytes'] for p in pk))} of .nupkg files\n")
out.append("Curated ids come from `packages.yaml`; everything else is a dependency declared in a curated package's `.nuspec` and mirrored automatically.\n")
out.append("| id | version | why | .nupkg | payload | dependencies | license |")
out.append("|---|---|---|---|---|---|---|")
for p in pk:
    deps = "<br>".join(f"{d['id']} `{d['range'] or '*'}`" for d in p["dependencies"]) or "—"
    if not p["has_install_script"]:
        payload = "metapackage (nuspec only)"
    elif p["embeds_binary"]:
        payload = "**embedded**: " + ", ".join(Path(f).name for f in p["embedded_files"][:3]) + (" …" if len(p["embedded_files"]) > 3 else "")
    else:
        payload = "link-only (downloads from vendor)"
    lic = f"[license]({p['license_url']})" if p["license_url"] else "—"
    out.append(f"| {p['id']} | {p['version']} | {p['reason']} | {mb(p['size_bytes'])} | {payload} | {deps} | {lic} |")
out.append("\n## Vendor download URLs (from tools/chocolateyInstall.ps1)\n")
out.append("What the endpoint will fetch at install time. Checksums are the ones pinned in the community script; if the vendor replaces the file in place, the install fails until the community package is updated and re-synced.\n")
for p in pk:
    if not p["vendor_urls"]:
        continue
    out.append(f"### {p['id']} {p['version']}")
    for u in p["vendor_urls"]:
        out.append(f"- {u}")
    if p["vendor_checksums"]:
        out.append("- checksums: " + ", ".join(f"`{k}={v}`" for k, v in p["vendor_checksums"].items()))
    out.append("")
out.append("## Provenance per file\n")
out.append("| file | sha256 (ours) | community hash | published |")
out.append("|---|---|---|---|")
for p in pk:
    out.append(f"| {p['file']} | `{p['sha256'][:16]}…` | {p['community']['package_hash_algorithm']} `{p['community']['package_hash'][:16]}…` | {p['community']['published'][:10]} |")
(ROOT / "CATALOG.md").write_text("\n".join(out) + "\n")
print("CATALOG.md written")
