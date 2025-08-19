# Super Fast Logo Scraper - No Hanging
param([string]$OutputDir = "football_logos")

# Create output directory
if (!(Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null }

# Essential missing teams with verified Wikipedia URLs
$quickDownloads = @{
    "Eintracht Frankfurt" = @("Germany", "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Eintracht_Frankfurt_Logo.svg/100px-Eintracht_Frankfurt_Logo.svg.png")
    "VfL Wolfsburg" = @("Germany", "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/VfL_Wolfsburg_Logo.svg/100px-VfL_Wolfsburg_Logo.svg.png")
    "SC Freiburg" = @("Germany", "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/SC_Freiburg_logo.svg/100px-SC_Freiburg_logo.svg.png")
    "Lens" = @("France", "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/RC_Lens_logo.svg/100px-RC_Lens_logo.svg.png")
    "Marseille" = @("France", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Olympique_de_Marseille_logo.svg/100px-Olympique_de_Marseille_logo.svg.png")
    "Monaco" = @("France", "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/AS_Monaco_FC.svg/100px-AS_Monaco_FC.svg.png")
    "Lille" = @("France", "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/LOSC_Lille_logo.svg/100px-LOSC_Lille_logo.svg.png")
    "Lyon" = @("France", "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Olympique_lyonnais_%28logo%29.svg/100px-Olympique_lyonnais_%28logo%29.svg.png")
    "Nice" = @("France", "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/OGC_Nice_logo.svg/100px-OGC_Nice_logo.svg.png")
    "Villarreal" = @("Spain", "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Villarreal_CF_logo.svg/100px-Villarreal_CF_logo.svg.png")
    "Osasuna" = @("Spain", "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/CA_Osasuna_logo.svg/100px-CA_Osasuna_logo.svg.png")
    "Aston Villa" = @("England", "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/100px-Aston_Villa_FC_crest_%282016%29.svg.png")
    "Crystal Palace" = @("England", "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Crystal_Palace_FC_logo_%282022%29.svg/100px-Crystal_Palace_FC_logo_%282022%29.svg.png")
    "Fulham" = @("England", "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Fulham_FC_%28shield%29.svg/100px-Fulham_FC_%28shield%29.svg.png")
    "Juventus" = @("Italy", "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Juventus_FC_2017_logo.svg/100px-Juventus_FC_2017_logo.svg.png")
    "Atalanta" = @("Italy", "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/Atalanta_BC_logo.svg/100px-Atalanta_BC_logo.svg.png")
    "Fiorentina" = @("Italy", "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/ACF_Fiorentina.svg/100px-ACF_Fiorentina.svg.png")
    "Bologna" = @("Italy", "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Bologna_FC_1909_logo.svg/100px-Bologna_FC_1909_logo.svg.png")
    "Torino" = @("Italy", "https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/Torino_FC_Logo.svg/100px-Torino_FC_Logo.svg.png")
    "Sporting CP" = @("Portugal", "https://upload.wikimedia.org/wikipedia/en/thumb/3/32/Sporting_Clube_de_Portugal_%28Logo%29.svg/100px-Sporting_Clube_de_Portugal_%28Logo%29.svg.png")
    "Braga" = @("Portugal", "https://upload.wikimedia.org/wikipedia/en/thumb/1/18/SC_Braga_logo.svg/100px-SC_Braga_logo.svg.png")
    "Corinthians" = @("Brazil", "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Corinthians_logo.svg/100px-Corinthians_logo.svg.png")
    "Santos" = @("Brazil", "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Santos_logo.svg/100px-Santos_logo.svg.png")
    "Atletico Mineiro" = @("Brazil", "https://upload.wikimedia.org/wikipedia/en/thumb/c/ca/Atletico_mineiro_galo.png/100px-Atletico_mineiro_galo.png")
    "Fluminense" = @("Brazil", "https://upload.wikimedia.org/wikipedia/en/thumb/0/05/Fluminense_fc_logo.svg/100px-Fluminense_fc_logo.svg.png")
    "Gremio" = @("Brazil", "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Gremio_logo.svg/100px-Gremio_logo.svg.png")
    "Rangers" = @("Scotland", "https://upload.wikimedia.org/wikipedia/en/thumb/8/88/Rangers_FC.svg/100px-Rangers_FC.svg.png")
    "Hearts" = @("Scotland", "https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/Heart_of_Midlothian_FC_logo.svg/100px-Heart_of_Midlothian_FC_logo.svg.png")
    "Aberdeen" = @("Scotland", "https://upload.wikimedia.org/wikipedia/en/thumb/8/8e/Aberdeen_FC.svg/100px-Aberdeen_FC.svg.png")
    "Hibernian" = @("Scotland", "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Hibernian_FC_logo.svg/100px-Hibernian_FC_logo.svg.png")
    "Galatasaray" = @("Turkey", "https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Galatasaray_Sports_Club_Logo.svg/100px-Galatasaray_Sports_Club_Logo.svg.png")
    "Fenerbahce" = @("Turkey", "https://upload.wikimedia.org/wikipedia/en/thumb/8/8b/Fenerbah%C3%A7e_SK_Logo.svg/100px-Fenerbah%C3%A7e_SK_Logo.svg.png")
    "Besiktas" = @("Turkey", "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Be%C5%9Fikta%C5%9F_JK_logo.svg/100px-Be%C5%9Fikta%C5%9F_JK_logo.svg.png")
    "Trabzonspor" = @("Turkey", "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Trabzonspor_logo.svg/100px-Trabzonspor_logo.svg.png")
    "Al Hilal" = @("Saudi_Arabia", "https://upload.wikimedia.org/wikipedia/en/thumb/1/1b/Al_Hilal_SFC_logo.svg/100px-Al_Hilal_SFC_logo.svg.png")
    "Al Nassr" = @("Saudi_Arabia", "https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Al_Nassr_FC_logo.svg/100px-Al_Nassr_FC_logo.svg.png")
    "Al Ittihad" = @("Saudi_Arabia", "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Al-Ittihad_Club_logo.svg/100px-Al-Ittihad_Club_logo.svg.png")
    "Al Ahli" = @("Saudi_Arabia", "https://upload.wikimedia.org/wikipedia/en/thumb/1/16/Al-Ahli_Saudi_FC_logo.svg/100px-Al-Ahli_Saudi_FC_logo.svg.png")
    "Young Boys" = @("Switzerland", "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/BSC_Young_Boys_logo.svg/100px-BSC_Young_Boys_logo.svg.png")
    "FC Zurich" = @("Switzerland", "https://upload.wikimedia.org/wikipedia/en/thumb/1/1a/FC_Z%C3%BCrich_logo.svg/100px-FC_Z%C3%BCrich_logo.svg.png")
    "Basel" = @("Switzerland", "https://upload.wikimedia.org/wikipedia/en/thumb/8/83/FC_Basel_1893_logo.svg/100px-FC_Basel_1893_logo.svg.png")
    "St Gallen" = @("Switzerland", "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/FC_St._Gallen_logo.svg/100px-FC_St._Gallen_logo.svg.png")
    "Olympiacos" = @("Greece", "https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Olympiacos_CFP_logo.svg/100px-Olympiacos_CFP_logo.svg.png")
    "PAOK" = @("Greece", "https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/PAOK_FC_logo.svg/100px-PAOK_FC_logo.svg.png")
    "AEK Athens" = @("Greece", "https://upload.wikimedia.org/wikipedia/en/thumb/7/7c/AEK_Athens_F.C._logo.svg/100px-AEK_Athens_F.C._logo.svg.png")
    "Panathinaikos" = @("Greece", "https://upload.wikimedia.org/wikipedia/en/thumb/1/1d/Panathinaikos_FC_logo.svg/100px-Panathinaikos_FC_logo.svg.png")
    "LA Galaxy" = @("USA", "https://upload.wikimedia.org/wikipedia/en/thumb/2/21/LA_Galaxy_logo.svg/100px-LA_Galaxy_logo.svg.png")
    "LAFC" = @("USA", "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/Los_Angeles_FC_logo.svg/100px-Los_Angeles_FC_logo.svg.png")
    "Seattle Sounders" = @("USA", "https://upload.wikimedia.org/wikipedia/en/thumb/1/15/Seattle_Sounders_FC_logo.svg/100px-Seattle_Sounders_FC_logo.svg.png")
    "Inter Miami" = @("USA", "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Inter_Miami_CF_logo.svg/100px-Inter_Miami_CF_logo.svg.png")
    "Atlanta United" = @("USA", "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/Atlanta_United_FC_logo.svg/100px-Atlanta_United_FC_logo.svg.png")
    "Philadelphia Union" = @("USA", "https://upload.wikimedia.org/wikipedia/en/thumb/6/6d/Philadelphia_Union_logo.svg/100px-Philadelphia_Union_logo.svg.png")
}

# Quick download function
function Quick-Download($team, $data) {
    $league = $data[0]
    $url = $data[1]
    
    $cleanName = $team -replace '[<>:"/\\|?*]', '_'
    $leagueDir = Join-Path $OutputDir $league
    if (!(Test-Path $leagueDir)) { New-Item -ItemType Directory -Path $leagueDir -Force | Out-Null }
    
    $filepath = Join-Path $leagueDir "$cleanName.png"
    
    if (Test-Path $filepath) {
        Write-Host "✓ $team" -ForegroundColor Gray
        return $true
    }
    
    try {
        Write-Host "⬇ $team" -ForegroundColor Yellow
        $webClient = New-Object System.Net.WebClient
        $webClient.Headers.Add("User-Agent", "Mozilla/5.0")
        $webClient.DownloadFile($url, $filepath)
        $webClient.Dispose()
        Write-Host "✅ $team" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ $team" -ForegroundColor Red
        return $false
    }
}

# Process downloads
$success = 0
$total = $quickDownloads.Count

Write-Host "🚀 Super Fast Logo Scraper" -ForegroundColor Cyan
Write-Host "Downloading $total team logos..." -ForegroundColor Yellow

foreach ($team in $quickDownloads.Keys) {
    if (Quick-Download $team $quickDownloads[$team]) {
        $success++
    }
    # No sleep - maximize speed
}

Write-Host "`n📊 Results: $success/$total downloaded" -ForegroundColor Cyan

# Quick final count without hanging commands
$existingFiles = 0
$countries = @("Germany", "France", "Spain", "England", "Italy", "Portugal", "Brazil", "Scotland", "Turkey", "Saudi_Arabia", "Switzerland", "Greece", "USA")

Write-Host "`n📁 Current collection:" -ForegroundColor Green
foreach ($country in $countries) {
    $countryPath = Join-Path $OutputDir $country
    if (Test-Path $countryPath) {
        $files = @(Get-ChildItem $countryPath -Filter "*.png" -ErrorAction SilentlyContinue)
        if ($files.Count -gt 0) {
            $existingFiles += $files.Count
            Write-Host "  $country`: $($files.Count) logos" -ForegroundColor White
        }
    }
}

Write-Host "`n🎯 TOTAL COLLECTION: $existingFiles logos!" -ForegroundColor Green

$percentage = [math]::Round(($existingFiles / 100) * 100, 1)
if ($existingFiles -ge 80) {
    Write-Host "🏆 EXCELLENT! Amazing collection achieved!" -ForegroundColor Green
} elseif ($existingFiles -ge 60) {
    Write-Host "🟢 GREAT! Strong collection!" -ForegroundColor Yellow  
} elseif ($existingFiles -ge 40) {
    Write-Host "🟡 GOOD! Solid progress!" -ForegroundColor Yellow
} else {
    Write-Host "🔄 Keep going for more logos!" -ForegroundColor Cyan
}

Write-Host "`nFiles saved in: $((Get-Item $OutputDir).FullName)" -ForegroundColor Gray
