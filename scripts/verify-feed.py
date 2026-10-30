#!/usr/bin/env python3
"""Check the feed an env actually serves after a publish: scripts/verify-feed.py <env> <base_uri>.

1. Waits until <base_uri>catalog.json equals the local feed/catalog.json (the client-feed pod syncs every 5 minutes).
2. index.json lists the service resources.
3. Every catalog package is in flatcontainer and its .nupkg sha256 matches the catalog.
4. openframe-client: the gateway download for the env's version matches the pinned sha256.
"""
import hashlib
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCAL_CATALOG = ROOT / "feed" / "catalog.json"
SYNC_WAIT, STEP = 600, 20


def get(url, tries=3):
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"Cache-Control": "no-cache"}), timeout=120) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt == tries - 1:
                raise SystemExit(f"GET {url}: {e}")
            time.sleep(STEP)


def normalize(version):
    # NuGet flatcontainer paths use the normalized, lowercase version: no build metadata, no 4th part of 0.
    parts = version.split("+")[0].lower().split(".")
    return ".".join(parts[:3] if len(parts) == 4 and parts[3] == "0" else parts)


def wait_for_sync(base):
    want = LOCAL_CATALOG.read_bytes()
    deadline = time.time() + SYNC_WAIT
    while True:
        try:
            if get(base + "catalog.json", tries=1) == want:
                return
        except SystemExit:
            pass
        if time.time() > deadline:
            raise SystemExit(f"{base}catalog.json does not match this build after {SYNC_WAIT}s")
        time.sleep(STEP)


def main():
    env, base = sys.argv[1], sys.argv[2]
    wait_for_sync(base)
    print(f"synced: {base}catalog.json")

    resources = json.loads(get(base + "index.json")).get("resources", [])
    if not resources:
        raise SystemExit(f"{base}index.json has no resources")

    errors = []
    for p in json.loads(LOCAL_CATALOG.read_text())["packages"]:
        pid, ver = p["id"].lower(), normalize(p["version"])
        if ver not in json.loads(get(f"{base}flatcontainer/{pid}/index.json")).get("versions", []):
            errors.append(f"{p['id']} {ver}: not in flatcontainer/{pid}/index.json")
            continue
        sha = hashlib.sha256(get(f"{base}flatcontainer/{pid}/{ver}/{pid}.{ver}.nupkg")).hexdigest()
        if sha != p["sha256"]:
            errors.append(f"{p['id']} {ver}: nupkg sha256 {sha} != catalog {p['sha256']}")
        else:
            print(f"ok {p['id']} {ver}")

    e = json.loads((ROOT / "packages/openframe-client/envs.json").read_text())[env]
    url = f"https://{e['host']}/v0/api/assets/download?agent=client&platform=windows&version={e['version']}"
    sha = hashlib.sha256(get(url, tries=10)).hexdigest()  # retries ride out an expired cached GitHub URL
    if sha != e["sha256"]:
        errors.append(f"openframe-client {e['version']}: download sha256 {sha} != envs.json {e['sha256']}")
    else:
        print(f"ok openframe-client download {e['version']} from {e['host']}")

    if errors:
        raise SystemExit("\n".join(errors))


if __name__ == "__main__":
    main()
