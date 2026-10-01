$ErrorActionPreference = 'Stop'
$toolsDir    = Split-Path -Parent $MyInvocation.MyCommand.Definition
$packageName = 'openframe-client'

# TODO(agent team): confirm the agent's own uninstall command; this assumes `openframe-client.exe uninstall`.
$exe = Join-Path $toolsDir "$packageName.exe"
if (Test-Path $exe) {
  $process = Start-Process -FilePath $exe -ArgumentList 'uninstall' -Wait -PassThru -NoNewWindow
  if ($process.ExitCode -ne 0) { Write-Warning "$packageName`: uninstall exited with code $($process.ExitCode); package files are removed anyway" }
} else {
  Write-Warning "$packageName`: $exe not present, nothing to run"
}
