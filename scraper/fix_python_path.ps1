# PowerShell script to add Python to PATH
$pythonPath = "C:\Users\void7\AppData\Local\Programs\Python\Python312"
$pythonScripts = "C:\Users\void7\AppData\Local\Programs\Python\Python312\Scripts"

Write-Host "Current PATH:" -ForegroundColor Yellow
$env:PATH -split ';' | ForEach-Object { Write-Host "  $_" }

Write-Host "`nAdding Python to PATH..." -ForegroundColor Yellow
Write-Host "Python path: $pythonPath" -ForegroundColor Green
Write-Host "Python Scripts path: $pythonScripts" -ForegroundColor Green

# Get current user PATH
$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User')

# Check if Python is already in PATH
if ($currentPath -notlike "*$pythonPath*") {
    # Add Python paths to user PATH
    $newPath = $currentPath + ";" + $pythonPath + ";" + $pythonScripts
    [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
    Write-Host "Python has been added to your PATH!" -ForegroundColor Green
    
    # Update current session PATH
    $env:PATH = $newPath + ";" + $env:PATH
} else {
    Write-Host "Python is already in PATH." -ForegroundColor Yellow
}

Write-Host "`nTesting Python installation..." -ForegroundColor Yellow
try {
    $result = & "$pythonPath\python.exe" --version 2>&1
    Write-Host "Python version: $result" -ForegroundColor Green
    Write-Host "Python is working correctly!" -ForegroundColor Green
} catch {
    Write-Host "Error testing Python: $_" -ForegroundColor Red
}

Write-Host "`nTesting 'python' command..." -ForegroundColor Yellow
try {
    $result = python --version 2>&1
    Write-Host "Result: $result" -ForegroundColor Green
} catch {
    Write-Host "'python' command not working yet. Please restart your PowerShell session." -ForegroundColor Yellow
}

Write-Host "`nPlease restart your PowerShell session for changes to take full effect." -ForegroundColor Yellow
