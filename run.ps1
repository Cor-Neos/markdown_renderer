# MDRender Launcher Script
# This script activates the virtual environment and runs the application

Write-Host "Starting MDRender..." -ForegroundColor Cyan

# Get the script's directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Activate virtual environment
$VenvActivate = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"

if (Test-Path $VenvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $VenvActivate
    
    # Run the application
    Write-Host "Launching application..." -ForegroundColor Green
    python (Join-Path $ScriptDir "main.py")
} else {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
