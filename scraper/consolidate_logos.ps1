# Consolidate all logo files into one folder
Write-Host "🏆 Consolidating all logo files into one folder..." -ForegroundColor Green

# Create the main consolidated folder
$consolidatedFolder = "all_league_logos"
if (!(Test-Path $consolidatedFolder)) {
    New-Item -ItemType Directory -Path $consolidatedFolder
    Write-Host "✓ Created folder: $consolidatedFolder" -ForegroundColor Yellow
}

# Get all PNG files from all subfolders
$sourceFolder = "ultimate_final_logos"
$allFiles = Get-ChildItem -Path $sourceFolder -Recurse -Filter "*.png"

Write-Host "📁 Found $($allFiles.Count) logo files to consolidate..." -ForegroundColor Cyan

# Move each file to the consolidated folder
$movedCount = 0
foreach ($file in $allFiles) {
    $newPath = Join-Path $consolidatedFolder $file.Name
    
    # If file with same name exists, add league prefix
    if (Test-Path $newPath) {
        $leagueName = $file.Directory.Name
        $fileNameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
        $fileExt = [System.IO.Path]::GetExtension($file.Name)
        $newFileName = "${leagueName}_${fileNameWithoutExt}${fileExt}"
        $newPath = Join-Path $consolidatedFolder $newFileName
    }
    
    Move-Item -Path $file.FullName -Destination $newPath -Force
    $movedCount++
    Write-Host "✓ Moved: $($file.Name)" -ForegroundColor Green
}

Write-Host "`n🎉 CONSOLIDATION COMPLETE!" -ForegroundColor Green
Write-Host "📊 Total files moved: $movedCount" -ForegroundColor Yellow
Write-Host "📁 All logos are now in: $consolidatedFolder" -ForegroundColor Cyan

# Show final count
$finalCount = (Get-ChildItem -Path $consolidatedFolder -Filter "*.png").Count
Write-Host "📈 Final count in consolidated folder: $finalCount" -ForegroundColor Yellow

Write-Host "`nDone."
