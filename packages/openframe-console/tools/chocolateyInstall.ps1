$ErrorActionPreference = 'Stop'

$packageArgs = @{
  packageName    = $env:ChocolateyPackageName
  fileType       = 'exe'
  url64bit       = 'https://github.com/flamingo-stack/openframe-oss-frontend/releases/download/1.0.193/OpenFrame-Console_1.0.193_x64-setup.exe'
  checksum64     = 'ef7bcda4fd49d9a20bc72879408a93487af3bd2ee3fd5a2f8b51a8a7bbe9848c'
  checksumType64 = 'sha256'
  silentArgs     = '/S'
  validExitCodes = @(0)
}

if ($env:PROCESSOR_ARCHITECTURE -eq 'ARM64') {
  $packageArgs.url64bit = 'https://github.com/flamingo-stack/openframe-oss-frontend/releases/download/1.0.193/OpenFrame-Console_1.0.193_arm64-setup.exe'
  $packageArgs.checksum64 = 'b929096779e60a69809bfb5740f35f8bbeb82cd93c66ed12bb4b9fcf72476f6b'
}

Install-ChocolateyPackage @packageArgs
