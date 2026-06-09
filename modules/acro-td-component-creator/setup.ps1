$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
[System.Environment]::SetEnvironmentVariable('ACRO_TD_COMPONENT_CREATOR', $ScriptDir, 'User')
$env:ACRO_TD_COMPONENT_CREATOR = $ScriptDir
Write-Host "ACRO_TD_COMPONENT_CREATOR set to $ScriptDir"
