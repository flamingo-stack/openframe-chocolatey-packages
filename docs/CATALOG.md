# Feed catalog

Source: `https://community.chocolatey.org/api/v2/` · generated 2026-09-29T15:26:45Z · 17 packages · 171.3 MB of .nupkg files

Curated ids come from `packages.yaml`; everything else is a dependency declared in a curated package's `.nuspec` and mirrored automatically.

| id | version | why | .nupkg | payload | dependencies | license |
|---|---|---|---|---|---|---|
| 7zip | 26.3.0 | curated | 4 KB | metapackage (nuspec only) | 7zip.install `[26.3.0]` | [license](http://www.7-zip.org/license.txt) |
| 7zip.install | 26.3.0 | dependency of 7zip | 2.9 MB | **embedded**: 7zip_x32.exe, 7zip_x64.exe | chocolatey-core.extension `1.3.3` | [license](http://www.7-zip.org/license.txt) |
| adobereader | 2026.2.21931 | curated | 9 KB | link-only (downloads from vendor) | kb2919355 `*` | [license](http://www.adobe.com/products/eulas/pdfs/Reader10_combined-20100625_1419.pdf) |
| chocolatey | 2.7.4 | curated | 5.4 MB | **embedded**: choco.exe, Chocolatey.PowerShell.dll, choco.exe … | — | [license](https://raw.githubusercontent.com/chocolatey/choco/master/LICENSE) |
| chocolatey-compatibility.extension | 1.0.0 | dependency of chocolatey-core.extension | 13 KB | metapackage (nuspec only) | — | [license](https://github.com/chocolatey-community/chocolatey-extensions/blob/master/LICENSE.md) |
| chocolatey-core.extension | 1.4.0 | dependency of GoogleChrome | 14 KB | metapackage (nuspec only) | chocolatey-compatibility.extension `1.0.0` | [license](https://github.com/chocolatey-community/chocolatey-extensions/blob/master/LICENSE.md) |
| Firefox | 156.0.1 | curated | 34 KB | link-only (downloads from vendor) | chocolatey-core.extension `1.3.3` | [license](https://www.mozilla.org/en-US/MPL/2.0/) |
| git | 2.56.0 | curated | 4 KB | metapackage (nuspec only) | git.install `[2.56.0]` | [license](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| git.install | 2.56.0 | dependency of git | 62.8 MB | **embedded**: Git-2.56.0-64-bit.exe | chocolatey-core.extension `1.3.3` | [license](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html) |
| GoogleChrome | 155.0.8059.12 | curated | 4 KB | link-only (downloads from vendor) | chocolatey-core.extension `1.3.3` | [license](https://www.google.it/intl/en/chrome/browser/privacy/eula_text.html) |
| KB2919355 | 1.0.20160915 | dependency of adobereader | 5 KB | link-only (downloads from vendor) | KB2919442 `1.0.20160915` | [license](https://support.microsoft.com/en-us/kb/2919355) |
| KB2919442 | 1.0.20160915 | dependency of KB2919355 | 4 KB | link-only (downloads from vendor) | — | [license](https://support.microsoft.com/en-us/kb/2919442) |
| notepadplusplus | 8.9.8.1 | curated | 4 KB | link-only (downloads from vendor) | notepadplusplus.install `[8.9.8.1]` | [license](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/LICENSE) |
| notepadplusplus.install | 8.9.8.1 | dependency of notepadplusplus | 13.0 MB | **embedded**: npp.8.9.8.1.Installer.exe, npp.8.9.8.1.Installer.x64.exe | chocolatey-core.extension `1.3.3` | [license](https://github.com/notepad-plus-plus/notepad-plus-plus/blob/master/LICENSE) |
| openframe-client | 1.0.0 | own | 3 KB | link-only (downloads from vendor) | — | [license](https://github.com/flamingo-stack/openframe-chocolatey-packages/blob/main/LICENSE) |
| vlc | 3.0.24 | curated | 3 KB | metapackage (nuspec only) | vlc.install `[3.0.24]` | [license](http://www.videolan.org/legal.html) |
| vlc.install | 3.0.24 | dependency of vlc | 87.1 MB | **embedded**: vlc-3.0.24-win32_x32.exe, vlc-3.0.24-win64_x64.exe | chocolatey-core.extension `1.3.3` | [license](http://www.videolan.org/legal.html) |

## Vendor download URLs (from tools/chocolateyInstall.ps1)

What the endpoint will fetch at install time. Checksums are the ones pinned in the community script; if the vendor replaces the file in place, the install fails until the community package is updated and re-synced.

### adobereader 2026.2.21931
- https://ardownload2.adobe.com/pub/adobe/acrobat/win/AcrobatDC/2600221931/AcroRdrDCx64Upd2600221931_MUI.msp
- https://ardownload2.adobe.com/pub/adobe/reader/win/AcrobatDC/2600221931/AcroRdrDCUpd2600221931_MUI.msp
- https://ardownload3.adobe.com/pub/adobe/acrobat/win/AcrobatDC/2600221931/AcroRdrDCx642600221931_MUI.exe
- https://ardownload3.adobe.com/pub/adobe/reader/win/AcrobatDC/2600221931/AcroRdrDC2600221931_MUI.exe
- https://www.adobe.com/devnet-docs/acrobatetk/tools/AdminGuide/properties.html#command-line-example

### chocolatey 2.7.4
- https://ch0.co/compatibility

### Firefox 156.0.1
- https://download.mozilla.org/?product=firefox-156.0.1-ssl&os=win&lang=${locale}
- https://download.mozilla.org/?product=firefox-156.0.1-ssl&os=win64&lang=${locale}
- https://download.mozilla.org/?product=firefox-156.0.1-ssl&os=win64-aarch64&lang=${locale}
- https://firefox-source-docs.mozilla.org/browser/installer/windows/installer/FullConfig.html
- https://github.com/chocolatey/chocolatey-coreteampackages/issues/933
- checksums: `checksumType=sha512`

### GoogleChrome 155.0.8059.12
- https://dl.google.com/dl/chrome/install/googlechromestandaloneenterprise.msi
- https://dl.google.com/dl/chrome/install/googlechromestandaloneenterprise64.msi
- checksums: `checksum=d3c5d9b99f9c5b6af88ba68e1063d576e889e218723adcaec687d147675bdd13`, `checksum64=40de51d92ebbc3d2e9b434526ec6f937bf9a62df6de7ca385dd02d0648379051`, `checksumType=sha256`, `checksumType64=sha256`

### KB2919355 1.0.20160915
- https://download.microsoft.com/download/2/5/6/256CCCFB-5341-4A8D-A277-8A81B21A1E35/Windows8.1-KB2919355-x64.msu
- https://download.microsoft.com/download/4/E/C/4EC66C83-1E15-43FD-B591-63FB7A1A5C04/Windows8.1-KB2919355-x86.msu
- https://download.microsoft.com/download/D/B/1/DB1F29FC-316D-481E-B435-1654BA185DCF/Windows8.1-KB2919355-x64.msu
- checksums: `checksum=F8BECA5B463A36E1FEF45AD0DCA6A0DE7606930380514AC1852DF5CA6E3F6C1D`, `checksum64=B0C9ADA530F5EE90BB962AFA9ED26218C582362315E13B1BA97E59767CB7825D`

### KB2919442 1.0.20160915
- https://download.microsoft.com/download/9/D/A/9DA6C939-9E65-4681-BBBE-A8F73A5C116F/Windows8.1-KB2919442-x86.msu
- https://download.microsoft.com/download/C/F/8/CF821C31-38C7-4C5C-89BB-B283059269AF/Windows8.1-KB2919442-x64.msu
- https://download.microsoft.com/download/D/6/0/D60ED3E0-93A5-4505-8F6A-8D0A5DA16C8A/Windows8.1-KB2919442-x64.msu
- checksums: `checksum=3368C3A329F402FD982B15B399368627B96973F008A5456B5286BDFC10C1169B`, `checksum64=C10787E669B484674584A990E069295E8B81B5366F98508010A3AE181B729482`

### openframe-client 1.0.0
- https://<ServerUrl>/v0/api/assets/download?agent=client&platform=windows

## Provenance per file

| file | sha256 (ours) | community hash | published |
|---|---|---|---|
| 7zip.26.3.0.nupkg | `ec96c6a0ab7a8b92…` | SHA512 `L0XW5df1XZ/da9YD…` | 2026-09-04 |
| 7zip.install.26.3.0.nupkg | `f3b583bb314aa05a…` | SHA512 `Ig8A6vYrJVJ8r86V…` | 2026-09-04 |
| adobereader.2026.2.21931.nupkg | `8606f4a47150744b…` | SHA512 `YeaDAmT0gwzIKc6W…` | 2026-09-21 |
| chocolatey.2.7.4.nupkg | `aec2dbd6ce91b737…` | SHA512 `DArKTucre9KjiuRF…` | 2026-08-19 |
| chocolatey-compatibility.extension.1.0.0.nupkg | `7e81bee5d6b0527b…` | SHA512 `cRfCv902OWoBUREO…` | 2022-04-07 |
| chocolatey-core.extension.1.4.0.nupkg | `52d3ae6bb595d0df…` | SHA512 `ePZsQlm8eur8F379…` | 2022-04-19 |
| Firefox.156.0.1.nupkg | `0bf7e59e6d84c8bc…` | SHA512 `LjjprlzAa06pN3x/…` | 2026-09-22 |
| git.2.56.0.nupkg | `da15d4a48e26ee70…` | SHA512 `nyB0IJyT63p7VwrA…` | 2026-09-29 |
| git.install.2.56.0.nupkg | `44e7a6f9cae3481d…` | SHA512 `B1ubZqQvYIBQIGp9…` | 2026-09-29 |
| GoogleChrome.155.0.8059.12.nupkg | `6101af289c205852…` | SHA512 `5MXZFgGsyBVQjDt3…` | 2026-09-24 |
| KB2919355.1.0.20160915.nupkg | `e4d1e19587bfc89a…` | SHA512 `RCCHts7pC4SV1kJd…` | 2016-09-20 |
| KB2919442.1.0.20160915.nupkg | `8d1c0b79ec22343f…` | SHA512 `TQeoUGG09UgFxQ8k…` | 2016-09-20 |
| notepadplusplus.8.9.8.1.nupkg | `4976015d538de733…` | SHA512 `w0I9rpodl/8IwlpU…` | 2026-09-24 |
| notepadplusplus.install.8.9.8.1.nupkg | `cb00e8b8a903e491…` | SHA512 `p7rpDwbh8r1jRbNu…` | 2026-09-24 |
| openframe-client.1.0.0.nupkg | `9b56e668c0867d17…` |  `…` |  |
| vlc.3.0.24.nupkg | `232076a7b499f22b…` | SHA512 `c/mirRIC/PfTe3EY…` | 2026-09-22 |
| vlc.install.3.0.24.nupkg | `c3f6d122d75d774f…` | SHA512 `gPlBzz9CI4bIFFKy…` | 2026-09-22 |
