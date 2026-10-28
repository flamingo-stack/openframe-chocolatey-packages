$ErrorActionPreference = 'Stop'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  fileType       = 'exe'
  url64bit       = 'https://github.com/flamingo-stack/openframe-oss-frontend/releases/download/1.0.196/OpenFrame-Console_1.0.196_x64-setup.exe'
  checksum64     = '07807c023270a12470596bd4e9283743cfa2dfa7ea826ff900709095a6458146'
  checksumType64 = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') {
  $packageArgs.url64bit = 'https://github.com/flamingo-stack/openframe-oss-frontend/releases/download/1.0.196/OpenFrame-Console_1.0.196_arm64-setup.exe'
  $packageArgs.checksum64 = 'eb0555bc05d146b8fc9809838cfb3af8fc84967fa95c92285e7d7176029f71ef'
}

Install-ChocolateyPackage @packageArgs
