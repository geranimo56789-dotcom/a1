# Final Logo Scraper - Maximum Success
param([string]$OutputDir = "football_logos")

if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

# Working URLs verified by testing
$workingUrls = @{
    "Eintracht Frankfurt" = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Eintracht_Frankfurt_Logo.svg/100px-Eintracht_Frankfurt_Logo.svg.png"
    "VfL Wolfsburg" = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/VfL_Wolfsburg_Logo.svg/100px-VfL_Wolfsburg_Logo.svg.png"
    "SC Freiburg" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/SC_Freiburg_logo.svg/100px-SC_Freiburg_logo.svg.png"
    "Werder Bremen" = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/SV_Werder_Bremen_logo.svg/100px-SV_Werder_Bremen_logo.svg.png"
    "Lens" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/RC_Lens_logo.svg/100px-RC_Lens_logo.svg.png"
    "Marseille" = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Olympique_de_Marseille_logo.svg/100px-Olympique_de_Marseille_logo.svg.png"
    "Rennes" = "https://upload.wikimedia.org/wikipedia/en/thumb/2/22/Stade_Rennais_FC.svg/100px-Stade_Rennais_FC.svg.png"
    "Monaco" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/AS_Monaco_FC.svg/100px-AS_Monaco_FC.svg.png"
    "Lille" = "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/LOSC_Lille_logo.svg/100px-LOSC_Lille_logo.svg.png"
    "Lyon" = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Olympique_lyonnais_%28logo%29.svg/100px-Olympique_lyonnais_%28logo%29.svg.png"
    "Nice" = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/OGC_Nice_logo.svg/100px-OGC_Nice_logo.svg.png"
    "Villarreal" = "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Villarreal_CF_logo.svg/100px-Villarreal_CF_logo.svg.png"
    "Osasuna" = "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/CA_Osasuna_logo.svg/100px-CA_Osasuna_logo.svg.png"
    "Aston Villa" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/100px-Aston_Villa_FC_crest_%282016%29.svg.png"
    "Crystal Palace" = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/Crystal_Palace_FC_logo_%282022%29.svg/100px-Crystal_Palace_FC_logo_%282022%29.svg.png"
    "Juventus" = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Juventus_FC_2017_logo.svg/100px-Juventus_FC_2017_logo.svg.png"
    "Atalanta" = "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/Atalanta_BC_logo.svg/100px-Atalanta_BC_logo.svg.png"
    "Fiorentina" = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/ACF_Fiorentina.svg/100px-ACF_Fiorentina.svg.png"
    "Bologna" = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Bologna_FC_1909_logo.svg/100px-Bologna_FC_1909_logo.svg.png"
    "Sporting CP" = "https://upload.wikimedia.org/wikipedia/en/thumb/3/32/Sporting_Clube_de_Portugal_%28Logo%29.svg/100px-Sporting_Clube_de_Portugal_%28Logo%29.svg.png"
    "Braga" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/18/SC_Braga_logo.svg/100px-SC_Braga_logo.svg.png"
    "Corinthians" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Corinthians_logo.svg/100px-Corinthians_logo.svg.png"
    "Santos" = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Santos_logo.svg/100px-Santos_logo.svg.png"
    "Rangers" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/88/Rangers_FC.svg/100px-Rangers_FC.svg.png"
    "Hearts" = "https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/Heart_of_Midlothian_FC_logo.svg/100px-Heart_of_Midlothian_FC_logo.svg.png"
    "Aberdeen" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/8e/Aberdeen_FC.svg/100px-Aberdeen_FC.svg.png"
    "Galatasaray" = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Galatasaray_Sports_Club_Logo.svg/100px-Galatasaray_Sports_Club_Logo.svg.png"
    "Fenerbahce" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/8b/Fenerbah%C3%A7e_SK_Logo.svg/100px-Fenerbah%C3%A7e_SK_Logo.svg.png"
    "Besiktas" = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Be%C5%9Fikta%C5%9F_JK_logo.svg/100px-Be%C5%9Fikta%C5%9F_JK_logo.svg.png"
    "Al Hilal" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/1b/Al_Hilal_SFC_logo.svg/100px-Al_Hilal_SFC_logo.svg.png"
    "Al Nassr" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Al_Nassr_FC_logo.svg/100px-Al_Nassr_FC_logo.svg.png"
    "Young Boys" = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/BSC_Young_Boys_logo.svg/100px-BSC_Young_Boys_logo.svg.png"
    "Basel" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/83/FC_Basel_1893_logo.svg/100px-FC_Basel_1893_logo.svg.png"
    "Olympiacos" = "https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Olympiacos_CFP_logo.svg/100px-Olympiacos_CFP_logo.svg.png"
    "PAOK" = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/PAOK_FC_logo.svg/100px-PAOK_FC_logo.svg.png"
    "LA Galaxy" = "https://upload.wikimedia.org/wikipedia/en/thumb/2/21/LA_Galaxy_logo.svg/100px-LA_Galaxy_logo.svg.png"
    "LAFC" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/Los_Angeles_FC_logo.svg/100px-Los_Angeles_FC_logo.svg.png"
    "Seattle Sounders" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/15/Seattle_Sounders_FC_logo.svg/100px-Seattle_Sounders_FC_logo.svg.png"
    "Inter Miami" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Inter_Miami_CF_logo.svg/100px-Inter_Miami_CF_logo.svg.png"
}

$teamLeagues = @{
    "Eintracht Frankfurt" = "Germany"
    "VfL Wolfsburg" = "Germany"
    "SC Freiburg" = "Germany"
    "Werder Bremen" = "Germany"
    "Lens" = "France"
    "Marseille" = "France"
    "Rennes" = "France"
    "Monaco" = "France"
    "Lille" = "France"
    "Lyon" = "France"
    "Nice" = "France"
    "Villarreal" = "Spain"
    "Osasuna" = "Spain"
    "Aston Villa" = "England"
    "Crystal Palace" = "England"
    "Juventus" = "Italy"
    "Atalanta" = "Italy"
    "Fiorentina" = "Italy"
    "Bologna" = "Italy"
    "Sporting CP" = "Portugal"
    "Braga" = "Portugal"
    "Corinthians" = "Brazil"
    "Santos" = "Brazil"
    "Rangers" = "Scotland"
    "Hearts" = "Scotland"
    "Aberdeen" = "Scotland"
    "Galatasaray" = "Turkey"
    "Fenerbahce" = "Turkey"
    "Besiktas" = "Turkey"
    "Al Hilal" = "Saudi_Arabia"
    "Al Nassr" = "Saudi_Arabia"
    "Young Boys" = "Switzerland"
    "Basel" = "Switzerland"
    "Olympiacos" = "Greece"
    "PAOK" = "Greece"
    "LA Galaxy" = "USA"
    "LAFC" = "USA"
    "Seattle Sounders" = "USA"
    "Inter Miami" = "USA"
}

function Download-TeamLogo {
    param($TeamName, $Url, $League)
    
    $cleanName = $TeamName -replace '[<>:"/\\|?*]', '_'
    $leagueDir = Join-Path $OutputDir $League
    if (!(Test-Path $leagueDir)) {
        New-Item -ItemType Directory -Path $leagueDir -Force | Out-Null
    }
    
    $filepath = Join-Path $leagueDir "$cleanName.png"
    
    if (Test-Path $filepath) {
        Write-Host "EXISTS: $TeamName" -ForegroundColor Gray
        return $true
    }
    
    try {
        Write-Host "DOWNLOADING: $TeamName" -ForegroundColor Yellow
        Invoke-WebRequest -Uri $Url -OutFile $filepath -TimeoutSec 10
        Write-Host "SUCCESS: $TeamName" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "FAILED: $TeamName" -ForegroundColor Red
        return $false
    }
}

$successful = 0
$total = $workingUrls.Count

Write-Host "🏈 Final Logo Scraper - Completing Collection" -ForegroundColor Cyan
Write-Host "Processing $total missing teams..." -ForegroundColor Yellow

foreach ($team in $workingUrls.Keys) {
    $league = $teamLeagues[$team]
    if (Download-TeamLogo $team $workingUrls[$team] $league) {
        $successful++
    }
    Start-Sleep -Milliseconds 200
}

Write-Host "`n📊 Final Batch: $successful/$total" -ForegroundColor Cyan

# Count all files now
$allFiles = 0
$leagues = @("Germany", "France", "Spain", "England", "Italy", "Portugal", "Brazil", "Scotland", "Turkey", "Saudi_Arabia", "Switzerland", "Greece", "USA")

foreach ($league in $leagues) {
    $leagueDir = Join-Path $OutputDir $league
    if (Test-Path $leagueDir) {
        $files = Get-ChildItem $leagueDir -Filter "*.png"
        $allFiles += $files.Count
        if ($files.Count -gt 0) {
            Write-Host "$league`: $($files.Count) files" -ForegroundColor White
        }
    }
}

Write-Host "`nGRAND TOTAL: $allFiles logos downloaded!" -ForegroundColor Green

if ($allFiles -ge 70) {
    Write-Host "🎉 EXCELLENT! Great collection achieved!" -ForegroundColor Green
} elseif ($allFiles -ge 60) {
    Write-Host "🟢 GOOD! Strong collection!" -ForegroundColor Yellow
} else {
    Write-Host "🔄 Run again for more logos" -ForegroundColor Yellow
}
