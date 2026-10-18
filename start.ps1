# Usage:  .\start.ps1 3      -> starts project 03 (API on :8003, web on :5173)
#         .\start.ps1 all    -> starts all seven projects + opens the hub page
param([string]$Project = "all")
$root = $PSScriptRoot
$python = Join-Path $root ".venv\Scripts\python.exe"
$dirs = Get-ChildItem $root -Directory | Where-Object { $_.Name -match '^0[1-7]-' } | Sort-Object Name
if ($Project -ne "all") { $dirs = $dirs | Where-Object { [int]$_.Name.Substring(0, 2) -eq [int]$Project } }

foreach ($d in $dirs) {
  $n = [int]$d.Name.Substring(0, 2)
  $api = 8000 + $n
  $web = 5170 + $n
  Start-Process powershell -WorkingDirectory "$($d.FullName)\backend" -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle='$($d.Name) API :$api'; & '$python' -m uvicorn main:app --reload --port $api"
  Start-Process powershell -WorkingDirectory "$($d.FullName)\frontend" -ArgumentList "-NoExit", "-Command", "`$host.UI.RawUI.WindowTitle='$($d.Name) WEB :$web'; npm run dev"
  Write-Host ("{0,-32} web http://localhost:{1}   api http://localhost:{2}/docs" -f $d.Name, $web, $api) -ForegroundColor Cyan
}
if ($Project -eq "all") { Start-Process (Join-Path $root "index.html") }
