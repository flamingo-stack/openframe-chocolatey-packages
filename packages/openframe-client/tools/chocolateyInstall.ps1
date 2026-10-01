$ErrorActionPreference = 'Stop'
$toolsDir    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$packageName = 'openframe-client'

# --params "/ServerUrl:host /InitialKey:... /OrgId:... /UserId:... [/MachineId:guid]"
$pp = Get-PackageParameters
foreach ($required in 'ServerUrl', 'InitialKey', 'OrgId', 'UserId') {
  if (-not $pp[$required]) { throw "$packageName`: missing required package parameter /$required" }
}
$serverUrl = ($pp['ServerUrl'] -replace '^https?://', '').TrimEnd('/')
$machineId = if ($pp['MachineId']) { $pp['MachineId'] } else { [guid]::NewGuid().ToString() }

# Same download the manual bootstrap script does: the tenant's asset endpoint, keyed by machine id.
# https + tenant host means no checksum can be pinned here: the endpoint always serves the tenant's current build.
$zip = Join-Path $toolsDir "$packageName.zip"
Get-ChocolateyWebFile -PackageName $packageName -FileFullPath $zip `
  -Url "https://$serverUrl/v0/api/assets/download?agent=client&platform=windows" `
  -Options @{ Headers = @{ 'x-machine-id' = $machineId } }

Get-ChocolateyUnzip -FileFullPath $zip -Destination $toolsDir -PackageName $packageName
Remove-Item $zip -Force -ErrorAction SilentlyContinue

$exe = Join-Path $toolsDir "$packageName.exe"
if (-not (Test-Path $exe)) { throw "$packageName`: $exe not found after unzip" }
# the exe is an installer/CLI, not a tool users call: no shim in C:\ProgramData\chocolatey\bin
New-Item -Path "$exe.ignore" -ItemType File -Force | Out-Null

$arguments = @(
  'install',
  '--serverUrl',  $serverUrl,
  '--initialKey', $pp['InitialKey'],
  '--orgId',      $pp['OrgId'],
  '--userId',     $pp['UserId']
)
Write-Host "$packageName`: enrolling machine $machineId with $serverUrl"
$process = Start-Process -FilePath $exe -ArgumentList $arguments -Wait -PassThru -NoNewWindow
if ($process.ExitCode -ne 0) { throw "$packageName`: install exited with code $($process.ExitCode)" }

# remembered for uninstall and for re-runs of the package
@{ ServerUrl = $serverUrl; MachineId = $machineId } | ConvertTo-Json | Set-Content (Join-Path $toolsDir 'enrollment.json')
