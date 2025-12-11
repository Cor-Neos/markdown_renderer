# Build Script for MDRender
# This script builds the application into a standalone executable using PyInstaller

Write-Host "Building MDRender executable..." -ForegroundColor Cyan

# Get the script's directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# Activate virtual environment
$VenvActivate = Join-Path $ScriptDir ".venv\Scripts\Activate.ps1"

if (Test-Path $VenvActivate) {
    Write-Host "Activating virtual environment..." -ForegroundColor Green
    & $VenvActivate
    
    # Check if PyInstaller is installed
    $PyInstallerCheck = pip show pyinstaller 2>$null
    if (-not $PyInstallerCheck) {
        Write-Host "PyInstaller not found. Installing..." -ForegroundColor Yellow
        pip install pyinstaller
    }
    
    # Clean previous build
    if (Test-Path "build") {
        Write-Host "Cleaning previous build..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "build"
    }
    if (Test-Path "dist") {
        Write-Host "Cleaning previous dist..." -ForegroundColor Yellow
        Remove-Item -Recurse -Force "dist"
    }
    
    # Build using spec file
    Write-Host "Building executable..." -ForegroundColor Green
    pyinstaller MDRender.spec --clean
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nBuild completed successfully!" -ForegroundColor Green
        Write-Host "Executable location: dist\MDRender\MDRender.exe" -ForegroundColor Cyan
        Write-Host "`nYou can now run the application from: dist\MDRender\" -ForegroundColor Yellow
    } else {
        Write-Host "`nBuild failed! Check the errors above." -ForegroundColor Red
    }
} else {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create a virtual environment first." -ForegroundColor Yellow
    exit 1
}

Write-Host "`nPress Enter to exit..." -ForegroundColor Gray
Read-Host
