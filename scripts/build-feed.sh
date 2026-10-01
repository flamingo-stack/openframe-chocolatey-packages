#!/usr/bin/env bash
# Build a static NuGet v3 feed from downloads/ with Sleet.
#   scripts/build-feed.sh <out_dir> <base_uri>
# base_uri is baked into every URL of the feed: it must be the URL clients use (the gateway route),
# never the bucket. Requires `sleet` on PATH (dotnet tool install -g sleet).
set -euo pipefail
out="${1:?out_dir}"; base="${2:?base_uri}"
root="$(cd "$(dirname "$0")/.." && pwd)"
cfg="$(mktemp)"
cat > "$cfg" <<JSON
{ "sources": [ { "name": "feed", "type": "local", "path": "$(cd "$root" && mkdir -p "$out" && cd "$out" && pwd)", "baseURI": "$base" } ] }
JSON
rm -rf "$root/$out"; mkdir -p "$root/$out"
sleet init     --config "$cfg" --source feed
sleet push     --config "$cfg" --source feed "$root/downloads/"
sleet validate --config "$cfg" --source feed
rm -f "$cfg"
echo "feed built at $root/$out for $base"
