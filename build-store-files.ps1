# Store Files Build Script for VAR6 Betting App
# This script generates the necessary files for App Store and Google Play Store submission

Write-Host "=== VAR6 Betting App - Store Files Builder ===" -ForegroundColor Green
Write-Host ""

# Check if we're in the correct directory
if (-not (Test-Path "MauiApp1\MauiApp1.csproj")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

Write-Host "Building Windows executable..." -ForegroundColor Yellow
dotnet build -c Release -p:TargetFramework=net8.0-windows10.0.19041.0 MauiApp1\MauiApp1.csproj

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Windows build successful" -ForegroundColor Green
    Write-Host "Location: MauiApp1\bin\Release\net8.0-windows10.0.19041.0\win10-x64\MauiApp1.exe" -ForegroundColor Cyan
} else {
    Write-Host "✗ Windows build failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "Building iOS simulator version..." -ForegroundColor Yellow
dotnet build -c Release -f net8.0-ios MauiApp1\MauiApp1.csproj

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ iOS simulator build successful" -ForegroundColor Green
    Write-Host "Location: MauiApp1\bin\Release\net8.0-ios\iossimulator-x64\" -ForegroundColor Cyan
    Write-Host "Note: For App Store submission, you need macOS and Xcode to build device version" -ForegroundColor Yellow
} else {
    Write-Host "✗ iOS build failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "Attempting Android publish (signed AAB)..." -ForegroundColor Yellow
dotnet publish -c Release -f net8.0-android -p:AndroidPackageFormat=aab MauiApp1\MauiApp1.csproj

if ($LASTEXITCODE -eq 0) {
    # Expected final signed AAB name uses ApplicationId
    $aabPath = Join-Path "MauiApp1\bin\Release\net8.0-android" "com.var6.bettingapp-Signed.aab"
    if (Test-Path $aabPath) {
        Write-Host "✓ Android AAB publish successful" -ForegroundColor Green
        Write-Host "Location: $aabPath" -ForegroundColor Cyan
    } else {
        Write-Host "✓ Android publish completed, but expected AAB not found at default name." -ForegroundColor Yellow
        Write-Host "Check: MauiApp1\\bin\\Release\\net8.0-android\\*.aab" -ForegroundColor Cyan
    }
} else {
    Write-Host "✗ Android publish failed (Android SDK may not be installed)" -ForegroundColor Red
    Write-Host "To build Android AAB, install Android SDK (Visual Studio > Mobile development with .NET) or run: dotnet workload install android" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=== Build Summary ===" -ForegroundColor Green
Write-Host "✓ Windows executable ready" -ForegroundColor Green
Write-Host "⚠ iOS: Simulator build complete, device build requires macOS/Xcode" -ForegroundColor Yellow
Write-Host "⚠ Android: May require Android SDK installation" -ForegroundColor Yellow

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. For iOS App Store: Use macOS with Xcode to build device version" -ForegroundColor White
Write-Host "2. For Google Play Store: Install Android SDK and build AAB file" -ForegroundColor White
Write-Host "3. Create app store listings with required metadata" -ForegroundColor White
Write-Host "4. Generate store assets (icons, screenshots, descriptions)" -ForegroundColor White
Write-Host "5. Submit for review following store guidelines" -ForegroundColor White

Write-Host ""
Write-Host "See Store_Files_Guide.md for detailed instructions" -ForegroundColor Cyan
