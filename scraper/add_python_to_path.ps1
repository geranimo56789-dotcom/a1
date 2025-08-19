# PowerShell script to add Python to PATH
Write-Host "Searching for Python installation..." -ForegroundColor Yellow

# Common Python installation locations
$pythonPaths = @(
    "C:\Python*",
    "C:\Program Files\Python*",
    "C:\Program Files (x86)\Python*",
    "$env:LOCALAPPDATA\Programs\Python*",
    "$env:APPDATA\Local\Programs\Python*"
)

$foundPython = $null

foreach ($path in $pythonPaths) {
    $pythonDirs = Get-ChildItem -Path $path -Directory -ErrorAction SilentlyContinue
    foreach ($dir in $pythonDirs) {
        $pythonExe = Join-Path $dir.FullName "python.exe"
        if (Test-Path $pythonExe) {
            $foundPython = $dir.FullName
            Write-Host "Found Python at: $foundPython" -ForegroundColor Green
            break
        }
    }
    if ($foundPython) { break }
}

if (-not $foundPython) {
    Write-Host "Python not found in common locations." -ForegroundColor Red
    Write-Host "Please manually find your Python installation directory and run:" -ForegroundColor Yellow
    Write-Host "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'User') + ';C:\path\to\python', 'User')" -ForegroundColor Cyan
    exit 1
}

# Add Python to user PATH
$currentPath = [Environment]::GetEnvironmentVariable('Path', 'User')
if ($currentPath -notlike "*$foundPython*") {
    $newPath = $currentPath + ";" + $foundPython
    [Environment]::SetEnvironmentVariable('Path', $newPath, 'User')
    Write-Host "Added Python to PATH: $foundPython" -ForegroundColor Green
    Write-Host "Please restart your command prompt for changes to take effect." -ForegroundColor Yellow
} else {
    Write-Host "Python is already in PATH." -ForegroundColor Green
}

# Test if it works
Write-Host "Testing Python installation..." -ForegroundColor Yellow
try {
    & "$foundPython\python.exe" --version
    Write-Host "Python is working correctly!" -ForegroundColor Green
} catch {
    Write-Host "Error testing Python: $_" -ForegroundColor Red
}
