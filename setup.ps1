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

Write-Host "Creating TD pref.txt file"

$Username = $env:USERNAME
# Construct the file path with the dynamic Python version
$FilePath = "C:\\Users\\$Username\\AppData\\Local\\Derivative\\TouchDesigner099\\pref.txt"
$PythonPath = "C:\\Users\\$Username\\AppData\\Local\\Programs\\Python\\Python311"
# Create content
$Content = @"
general.stopplayingwhenminimized	0
dats.texteditor	C:/Users/$Username/AppData/Local/Programs/Microsoft VS Code/Code.exe
general.playbarshortcuts	0
general.pythonpackages64	$PythonPath\\Lib\\site-packages
general.startupfilemode	1
chops.graphdisplay2	6
network.zoomdelay	0.19999999
network.zoomboost	1.0000002
"@

# correct line endings for TD
$Content = $Content.Replace("`r`n", "`n")

# Write content to file
$Content | Out-File -FilePath $FilePath -Encoding UTF8

# install python packages
Write-Host "Installing Python packages"
& "$PythonPath\python.exe" -m pip install --upgrade pip

# pip install requirements.txt
& "$PythonPath\Scripts\pip.exe" install -r "$ScriptDir\requirements.txt"

# The MCP server ships prebuilt (modules/acro-td-mcp/dist/index.js); it only needs Node
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Warning "Node.js was not found on PATH. Install it to use the acro-td-mcp MCP server."
}
