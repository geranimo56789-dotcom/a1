# Add Python to PATH
$pythonPath = "C:\Users\void7\AppData\Local\Programs\Python\Python312"
$pythonScripts = "C:\Users\void7\AppData\Local\Programs\Python\Python312\Scripts"

Write-Host "Adding Python to PATH..." -ForegroundColor Yellow
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
} else {
    Write-Host "Python is already in PATH." -ForegroundColor Yellow
}

Write-Host "Please restart your command prompt for changes to take effect." -ForegroundColor Yellow
Write-Host "After restarting, you can test with: python --version" -ForegroundColor Cyan

# Test the Python installation
Write-Host "Testing Python installation..." -ForegroundColor Yellow
try {
    & "$pythonPath\python.exe" --version
    Write-Host "Python is working correctly!" -ForegroundColor Green
} catch {
    Write-Host "Error testing Python: $_" -ForegroundColor Red
}
