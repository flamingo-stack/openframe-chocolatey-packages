#!/usr/bin/env bash
# Build a static NuGet v3 feed from downloads/ with Sleet: scripts/build-feed.sh <out_dir> <base_uri>
# base_uri is baked into every URL of the feed, so it must be the URL clients use. Needs `sleet` on PATH.
set -euo pipefail
out="${1:?out_dir}"; base="${2:?base_uri}"
cd "$(dirname "$0")/.."
rm -rf "${out:?}"; mkdir -p "$out"
cfg="$(mktemp)"
printf '{"sources":[{"name":"feed","type":"local","path":"%s","baseURI":"%s"}]}\n' "$PWD/$out" "$base" > "$cfg"
sleet init     --config "$cfg" --source feed
sleet push     --config "$cfg" --source feed downloads/
sleet validate --config "$cfg" --source feed
rm -f "$cfg"
echo "feed built at $out for $base"
