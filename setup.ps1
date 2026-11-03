# Set ACRO_TD_CORE environment variable
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
[System.Environment]::SetEnvironmentVariable('ACRO_TD_CORE', $ScriptDir, 'User')
$env:ACRO_TD_CORE = $ScriptDir
Write-Host "ACRO_TD_CORE set to $ScriptDir"

# Run all module setup scripts
Get-ChildItem -Path "$ScriptDir\modules\*\setup.ps1" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "Running $($_.Directory.Name)/setup.ps1"
    & $_.FullName
}

# Python packages (requirements.txt) are installed by TouchDesigner's tdPyEnvManager into the
# project's own venv the first time the .toe is opened (see TDPyEnvManagerContext.yaml)

# The MCP server ships prebuilt (modules/acro-td-mcp/dist/index.js); it only needs Node
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Warning "Node.js was not found on PATH. Install it to use the acro-td-mcp MCP server."
}
