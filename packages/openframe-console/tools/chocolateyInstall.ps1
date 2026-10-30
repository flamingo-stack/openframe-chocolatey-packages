$ErrorActionPreference = 'Stop'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  fileType       = 'exe'
  url64bit       = 'https://github.com/flamingo-stack/openframe-oss-frontend/releases/download/$version$/OpenFrame-Console_$version$_x64-setup.exe'
  checksum64     = '$sha256_x64$'
  checksumType64 = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') {
  $packageArgs.url64bit = 'https://github.com/flamingo-stack/openframe-oss-frontend/releases/download/$version$/OpenFrame-Console_$version$_arm64-setup.exe'
  $packageArgs.checksum64 = '$sha256_arm64$'
}

Install-ChocolateyPackage @packageArgs
