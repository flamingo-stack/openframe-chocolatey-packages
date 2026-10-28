$ErrorActionPreference = 'Stop'

[array]$key = Get-UninstallRegistryKey -SoftwareName 'OpenFrame Console'

if ($key.Count -eq 0) {
  Write-Warning 'OpenFrame Console is not installed for this user; nothing to uninstall.'
  return
}

foreach ($k in $key) {
  $null = Uninstall-ChocolateyPackage -PackageName $env:ChocolateyPackageName -FileType 'exe' -SilentArgs '/S' -File $k.UninstallString.Trim('"')
}
