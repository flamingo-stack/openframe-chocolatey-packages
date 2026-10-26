# openframe-chocolatey-packages

Source of the OpenFrame Chocolatey feed: a static NuGet v3 feed built by [Sleet](https://github.com/emgarten/Sleet) from
packages mirrored from `community.chocolatey.org` plus our own (`packages/`). Agents use it as a choco source:

| env | source URL | bucket |
|---|---|---|
| dev | `https://feed.openframe.build/choco/index.json` | `shared-j62b-client-feed` |
| stage | `https://feed.openframe.miami/choco/index.json` | `shared-d8ue-client-feed` |
| prod | `https://feed.openframe.ai/choco/index.json` | `shared-4t5d-client-feed` |

The feed lives under `choco/` of each env's client feed bucket (openframe-saas-tf `services/03-shared`). The bucket is
private; the `client-feed` chart in openframe-saas-shared (`manifests/platform/client-feed`) syncs `choco/` into nginx
every 5 minutes and serves it through the platform Gateway, so a publish is live within ~5 minutes.

## Layout

- `packages.yaml`: curated community ids. Dependencies declared in each `.nuspec` are mirrored too.
- `packages/<id>/`: our own packages (nuspec + `tools/`), e.g. [`openframe-client`](packages/openframe-client/README.md).
- `scripts/sync-community.py`: highest approved, non-prerelease version of each id from the v2 OData API
  (`IsLatestVersion` is unreliable), checked against the community `PackageHash`; follows dependencies, writes
  `downloads/` and `catalog.json`.
- `scripts/pack-own.py`: packs `packages/*` as OPC zips (no `choco pack` on Linux) into `downloads/`.
- `scripts/render-catalog.py`: `catalog.json` to `CATALOG.md` (payload, dependencies, vendor URLs, hashes).
- `scripts/build-feed.sh <out_dir> <base_uri>`: Sleet feed from `downloads/`. `base_uri` is baked into every URL, so
  each env gets its own build.

## CI: `.github/workflows/publish.yml`

Daily, on dispatch, and on PRs and pushes to `main` that touch packages or scripts.

| job | what |
|---|---|
| `build` | sync, pack, render (`CATALOG.md` goes to the run summary), test feed for `localhost`; artifact `packages` kept 30 days |
| `test_install` | Windows, choco 2.x: installs and uninstalls `TEST_PACKAGES` from the localhost feed only |
| `publish` | `main` only, one leg per env: builds the feed for its URL, `gcloud storage rsync --checksums-only --delete-unmatched-destination-objects` into `gs://<bucket>/choco/` |

No secrets: `google-github-actions/auth` uses each env's WIF provider (`shared/00-wif`), and `services/03-shared` grants
only `refs/heads/main` of this repo write on the `choco/` managed folder. The bucket keeps no versions; the next publish
is the rollback.

Local run of the first three scripts: `python3 scripts/sync-community.py && python3 scripts/pack-own.py && python3 scripts/render-catalog.py`.

## Notes

1. Link-only: community FOSS packages embed their installer (`git.install` 66 MB, `vlc.install` 91 MB, ...).
   `link_only` in the sync downloads each URL in `legal/VERIFICATION.txt`, pairs it with the embedded file by sha256,
   drops the file and prepends a `Get-ChocolateyWebFile` with that URL and sha256 to `chocolateyInstall.ps1`; an
   installer with no matching URL fails the sync. The feed is ~6 MB; only `chocolatey` keeps `choco.exe` (no vendor
   URL, and endpoints bootstrap choco from this feed). Rewritten packages no longer match the community `PackageHash`,
   which is checked before the rewrite.
2. `7zip`, `git`, `vlc`, `notepadplusplus` are metapackages pinning `<id>.install`; agents install the metapackage id.
3. `chocolatey-core.extension` is a dependency of almost everything; without it in the feed installs fail.
4. Chrome pins the sha256 of an unversioned vendor MSI that Google overwrites on release; community re-publishes within a
   day, so the sync runs daily.
