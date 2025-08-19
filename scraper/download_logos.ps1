# Football Logo Downloader
param([string]$OutputDir = "football_logos")

if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$teams = @{
    "Germany" = @("FC Bayern Munich", "Borussia Dortmund", "RB Leipzig", "Union Berlin", "Bayer Leverkusen", "Eintracht Frankfurt", "VfL Wolfsburg", "SC Freiburg", "Borussia Monchengladbach", "Werder Bremen")
    "France" = @("Paris Saint-Germain", "Lens", "Marseille", "Rennes", "Monaco", "Lille", "Lyon", "Nice", "Reims", "Montpellier")  
    "Spain" = @("Real Madrid", "Barcelona", "Atletico Madrid", "Real Sociedad", "Villarreal", "Real Betis", "Athletic Bilbao", "Sevilla", "Valencia", "Osasuna")
    "England" = @("Manchester City", "Arsenal", "Manchester United", "Liverpool", "Chelsea", "Newcastle United", "Tottenham", "Brighton", "Aston Villa", "West Ham")
    "Italy" = @("AC Milan", "Inter Milan", "Juventus", "Napoli", "AS Roma", "Lazio", "Atalanta", "Fiorentina", "Bologna", "Torino")
    "Portugal" = @("FC Porto", "Benfica", "Sporting CP", "Braga", "Vitoria Guimaraes", "Boavista")
    "Brazil" = @("Flamengo", "Palmeiras", "Sao Paulo", "Corinthians", "Santos", "Internacional", "Atletico Mineiro", "Botafogo")
    "Scotland" = @("Celtic", "Rangers", "Hearts", "Aberdeen", "Hibernian", "Motherwell")
    "Turkey" = @("Galatasaray", "Fenerbahce", "Besiktas", "Trabzonspor")
    "Saudi_Arabia" = @("Al Hilal", "Al Nassr", "Al Ittihad", "Al Ahli")
    "Switzerland" = @("Young Boys", "FC Zurich", "Basel", "St Gallen")
    "Greece" = @("Olympiacos", "PAOK", "AEK Athens", "Panathinaikos")
    "USA" = @("LA Galaxy", "LAFC", "Seattle Sounders", "Inter Miami", "New York Red Bulls", "Atlanta United")
}

$logoUrls = @{
    # Germany
    "FC Bayern Munich" = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg/100px-FC_Bayern_M%C3%BCnchen_logo_%282017%29.svg.png"
    "Borussia Dortmund" = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Borussia_Dortmund_logo.svg/100px-Borussia_Dortmund_logo.svg.png"
    "RB Leipzig" = "https://upload.wikimedia.org/wikipedia/en/thumb/0/04/RB_Leipzig_2014_logo.svg/100px-RB_Leipzig_2014_logo.svg.png"
    "Union Berlin" = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/1._FC_Union_Berlin_Logo.svg/100px-1._FC_Union_Berlin_Logo.svg.png"
    "Bayer Leverkusen" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/59/Bayer_04_Leverkusen_logo.svg/100px-Bayer_04_Leverkusen_logo.svg.png"
    "Eintracht Frankfurt" = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Eintracht_Frankfurt_Logo.svg/100px-Eintracht_Frankfurt_Logo.svg.png"
    "VfL Wolfsburg" = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/VfL_Wolfsburg_Logo.svg/100px-VfL_Wolfsburg_Logo.svg.png"
    "SC Freiburg" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/SC_Freiburg_logo.svg/100px-SC_Freiburg_logo.svg.png"
    
    # France
    "Paris Saint-Germain" = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Paris_Saint-Germain_F.C..svg/100px-Paris_Saint-Germain_F.C..svg.png"
    "Lens" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/RC_Lens_logo.svg/100px-RC_Lens_logo.svg.png"
    "Marseille" = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/Olympique_de_Marseille_logo.svg/100px-Olympique_de_Marseille_logo.svg.png"
    "Rennes" = "https://upload.wikimedia.org/wikipedia/en/thumb/2/22/Stade_Rennais_FC.svg/100px-Stade_Rennais_FC.svg.png"
    "Reims" = "https://upload.wikimedia.org/wikipedia/en/thumb/b/b2/Stade_de_Reims_logo.svg/100px-Stade_de_Reims_logo.svg.png"
    "Montpellier" = "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Montpellier_HSC_logo.svg/100px-Montpellier_HSC_logo.svg.png"
    "Monaco" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/AS_Monaco_FC.svg/100px-AS_Monaco_FC.svg.png"
    "Lille" = "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/LOSC_Lille_logo.svg/100px-LOSC_Lille_logo.svg.png"
    "Lyon" = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Olympique_lyonnais_%28logo%29.svg/100px-Olympique_lyonnais_%28logo%29.svg.png"
    "Nice" = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/OGC_Nice_logo.svg/100px-OGC_Nice_logo.svg.png"
    
    # Spain
    "Real Madrid" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/100px-Real_Madrid_CF.svg.png"
    "Barcelona" = "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/100px-FC_Barcelona_%28crest%29.svg.png"
    "Atletico Madrid" = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c1/Atletico_Madrid_logo.svg/100px-Atletico_Madrid_logo.svg.png"
    "Real Sociedad" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Real_Sociedad_logo.svg/100px-Real_Sociedad_logo.svg.png"
    "Villarreal" = "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Villarreal_CF_logo.svg/100px-Villarreal_CF_logo.svg.png"
    "Real Betis" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Real_betis_logo.svg/100px-Real_betis_logo.svg.png"
    "Athletic Bilbao" = "https://upload.wikimedia.org/wikipedia/en/thumb/9/98/Club_Athletic_Bilbao_logo.svg/100px-Club_Athletic_Bilbao_logo.svg.png"
    "Sevilla" = "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/Sevilla_FC_logo.svg/100px-Sevilla_FC_logo.svg.png"
    
    # England
    "Manchester City" = "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Manchester_City_FC_badge.svg/100px-Manchester_City_FC_badge.svg.png"
    "Arsenal" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/Arsenal_FC.svg/100px-Arsenal_FC.svg.png"
    "Manchester United" = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/100px-Manchester_United_FC_crest.svg.png"
    "Liverpool" = "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/100px-Liverpool_FC.svg.png"
    "Chelsea" = "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Chelsea_FC.svg/100px-Chelsea_FC.svg.png"
    "Newcastle United" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Newcastle_United_Logo.svg/100px-Newcastle_United_Logo.svg.png"
    "Tottenham" = "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/Tottenham_Hotspur.svg/100px-Tottenham_Hotspur.svg.png"
    "Brighton" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/fd/Brighton_%26_Hove_Albion_logo.svg/100px-Brighton_%26_Hove_Albion_logo.svg.png"
    
    # Italy
    "AC Milan" = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Logo_of_AC_Milan.svg/100px-Logo_of_AC_Milan.svg.png"
    "Inter Milan" = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/FC_Internazionale_Milano_2021.svg/100px-FC_Internazionale_Milano_2021.svg.png"
    "Juventus" = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Juventus_FC_2017_logo.svg/100px-Juventus_FC_2017_logo.svg.png"
    "Napoli" = "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/SSC_Neapel.svg/100px-SSC_Neapel.svg.png"
    "AS Roma" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/AS_Roma_logo_%282017%29.svg/100px-AS_Roma_logo_%282017%29.svg.png"
    "Lazio" = "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/S.S._Lazio_badge.svg/100px-S.S._Lazio_badge.svg.png"
    "Atalanta" = "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/Atalanta_BC_logo.svg/100px-Atalanta_BC_logo.svg.png"
    "Fiorentina" = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/ACF_Fiorentina.svg/100px-ACF_Fiorentina.svg.png"
    
    # Portugal
    "FC Porto" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/FC_Porto.svg/100px-FC_Porto.svg.png"
    "Benfica" = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a2/SL_Benfica_logo.svg/100px-SL_Benfica_logo.svg.png"
    "Sporting CP" = "https://upload.wikimedia.org/wikipedia/en/thumb/3/32/Sporting_Clube_de_Portugal_%28Logo%29.svg/100px-Sporting_Clube_de_Portugal_%28Logo%29.svg.png"
    "Braga" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/18/SC_Braga_logo.svg/100px-SC_Braga_logo.svg.png"
    
    # Brazil
    "Flamengo" = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Flamengo-RJ_%28BRA%29.png/100px-Flamengo-RJ_%28BRA%29.png"
    "Palmeiras" = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/Palmeiras_logo.svg/100px-Palmeiras_logo.svg.png"
    "Sao Paulo" = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Brasao_do_Sao_Paulo_Futebol_Clube.svg/100px-Brasao_do_Sao_Paulo_Futebol_Clube.svg.png"
    "Corinthians" = "https://upload.wikimedia.org/wikipedia/en/thumb/5/5a/Corinthians_logo.svg/100px-Corinthians_logo.svg.png"
    "Santos" = "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Santos_logo.svg/100px-Santos_logo.svg.png"
    "Internacional" = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Escudo_do_Sport_Club_Internacional.svg/100px-Escudo_do_Sport_Club_Internacional.svg.png"
    "Atletico Mineiro" = "https://upload.wikimedia.org/wikipedia/en/thumb/c/ca/Atletico_mineiro_galo.png/100px-Atletico_mineiro_galo.png"
    "Botafogo" = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Botafogo_de_Futebol_e_Regatas_logo.svg/100px-Botafogo_de_Futebol_e_Regatas_logo.svg.png"
    
    # Scotland
    "Celtic" = "https://upload.wikimedia.org/wikipedia/en/thumb/3/35/Celtic_FC.svg/100px-Celtic_FC.svg.png"
    "Rangers" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/88/Rangers_FC.svg/100px-Rangers_FC.svg.png"
    "Hearts" = "https://upload.wikimedia.org/wikipedia/en/thumb/d/d7/Heart_of_Midlothian_FC_logo.svg/100px-Heart_of_Midlothian_FC_logo.svg.png"
    "Aberdeen" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/8e/Aberdeen_FC.svg/100px-Aberdeen_FC.svg.png"
    "Hibernian" = "https://upload.wikimedia.org/wikipedia/en/thumb/e/eb/Hibernian_FC_logo.svg/100px-Hibernian_FC_logo.svg.png"
    "Motherwell" = "https://upload.wikimedia.org/wikipedia/en/thumb/6/66/Motherwell_FC_crest.svg/100px-Motherwell_FC_crest.svg.png"
    
    # Turkey
    "Galatasaray" = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7e/Galatasaray_Sports_Club_Logo.svg/100px-Galatasaray_Sports_Club_Logo.svg.png"
    "Fenerbahce" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/8b/Fenerbah%C3%A7e_SK_Logo.svg/100px-Fenerbah%C3%A7e_SK_Logo.svg.png"
    "Besiktas" = "https://upload.wikimedia.org/wikipedia/en/thumb/a/a7/Be%C5%9Fikta%C5%9F_JK_logo.svg/100px-Be%C5%9Fikta%C5%9F_JK_logo.svg.png"
    "Trabzonspor" = "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Trabzonspor_logo.svg/100px-Trabzonspor_logo.svg.png"
    
    # Saudi Arabia
    "Al Hilal" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/1b/Al_Hilal_SFC_logo.svg/100px-Al_Hilal_SFC_logo.svg.png"
    "Al Nassr" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f5/Al_Nassr_FC_logo.svg/100px-Al_Nassr_FC_logo.svg.png"
    "Al Ittihad" = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Al-Ittihad_Club_logo.svg/100px-Al-Ittihad_Club_logo.svg.png"
    "Al Ahli" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/16/Al-Ahli_Saudi_FC_logo.svg/100px-Al-Ahli_Saudi_FC_logo.svg.png"
    
    # Switzerland
    "Young Boys" = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e4/BSC_Young_Boys_logo.svg/100px-BSC_Young_Boys_logo.svg.png"
    "FC Zurich" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/1a/FC_Z%C3%BCrich_logo.svg/100px-FC_Z%C3%BCrich_logo.svg.png"
    "Basel" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/83/FC_Basel_1893_logo.svg/100px-FC_Basel_1893_logo.svg.png"
    "St Gallen" = "https://upload.wikimedia.org/wikipedia/en/thumb/3/3b/FC_St._Gallen_logo.svg/100px-FC_St._Gallen_logo.svg.png"
    
    # Greece
    "Olympiacos" = "https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Olympiacos_CFP_logo.svg/100px-Olympiacos_CFP_logo.svg.png"
    "PAOK" = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/PAOK_FC_logo.svg/100px-PAOK_FC_logo.svg.png"
    "AEK Athens" = "https://upload.wikimedia.org/wikipedia/en/thumb/7/7c/AEK_Athens_F.C._logo.svg/100px-AEK_Athens_F.C._logo.svg.png"
    "Panathinaikos" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/1d/Panathinaikos_FC_logo.svg/100px-Panathinaikos_FC_logo.svg.png"
    
    # USA
    "LA Galaxy" = "https://upload.wikimedia.org/wikipedia/en/thumb/2/21/LA_Galaxy_logo.svg/100px-LA_Galaxy_logo.svg.png"
    "LAFC" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/86/Los_Angeles_FC_logo.svg/100px-Los_Angeles_FC_logo.svg.png"
    "Seattle Sounders" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/15/Seattle_Sounders_FC_logo.svg/100px-Seattle_Sounders_FC_logo.svg.png"
    "Inter Miami" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Inter_Miami_CF_logo.svg/100px-Inter_Miami_CF_logo.svg.png"
    "New York Red Bulls" = "https://upload.wikimedia.org/wikipedia/en/thumb/6/6d/New_York_Red_Bulls_logo.svg/100px-New_York_Red_Bulls_logo.svg.png"
    "Atlanta United" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f7/Atlanta_United_FC_logo.svg/100px-Atlanta_United_FC_logo.svg.png"
    
    # Additional teams (non-duplicates)
    "Borussia Monchengladbach" = "https://upload.wikimedia.org/wikipedia/en/thumb/8/81/Borussia_M%C3%B6nchengladbach_logo.svg/100px-Borussia_M%C3%B6nchengladbach_logo.svg.png"
    "Werder Bremen" = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/SV_Werder_Bremen_logo.svg/100px-SV_Werder_Bremen_logo.svg.png"
    "Aston Villa" = "https://upload.wikimedia.org/wikipedia/en/thumb/f/f9/Aston_Villa_FC_crest_%282016%29.svg/100px-Aston_Villa_FC_crest_%282016%29.svg.png"
    "West Ham" = "https://upload.wikimedia.org/wikipedia/en/thumb/c/c2/West_Ham_United_FC_logo.svg/100px-West_Ham_United_FC_logo.svg.png"
    "Valencia" = "https://upload.wikimedia.org/wikipedia/en/thumb/c/ce/Valenciacf.svg/100px-Valenciacf.svg.png"
    "Osasuna" = "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/CA_Osasuna_logo.svg/100px-CA_Osasuna_logo.svg.png"
    "Bologna" = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Bologna_FC_1909_logo.svg/100px-Bologna_FC_1909_logo.svg.png"
    "Torino" = "https://upload.wikimedia.org/wikipedia/en/thumb/b/b8/Torino_FC_Logo.svg/100px-Torino_FC_Logo.svg.png"
    "Vitoria Guimaraes" = "https://upload.wikimedia.org/wikipedia/en/thumb/2/2d/Vit%C3%B3ria_de_Guimar%C3%A3es.svg/100px-Vit%C3%B3ria_de_Guimar%C3%A3es.svg.png"
    "Boavista" = "https://upload.wikimedia.org/wikipedia/en/thumb/1/16/Boavista_FC_logo.svg/100px-Boavista_FC_logo.svg.png"
}

$totalTeams = ($teams.Values | ForEach-Object { $_.Count } | Measure-Object -Sum).Sum
$downloaded = 0

Write-Host "Football Logo Downloader" -ForegroundColor Cyan
Write-Host "Total teams: $totalTeams" -ForegroundColor Yellow

foreach ($league in $teams.Keys) {
    $leagueDir = Join-Path $OutputDir $league
    if (!(Test-Path $leagueDir)) {
        New-Item -ItemType Directory -Path $leagueDir -Force | Out-Null
    }
    
    Write-Host ""
    Write-Host "Processing $league" -ForegroundColor Green
    
    foreach ($team in $teams[$league]) {
        $cleanName = $team -replace '[<>:"/\\|?*]', '_'
        $filename = $cleanName + '.png'
        $filepath = Join-Path $leagueDir $filename
        
        if (Test-Path $filepath) {
            Write-Host "EXISTS: $team" -ForegroundColor Gray
            $downloaded++
            continue
        }
        
        if ($logoUrls.ContainsKey($team)) {
            try {
                Write-Host "DOWNLOADING: $team" -ForegroundColor Yellow
                Invoke-WebRequest -Uri $logoUrls[$team] -OutFile $filepath -ErrorAction Stop
                Write-Host "SUCCESS: $team" -ForegroundColor Green
                $downloaded++
            } catch {
                Write-Host "FAILED: $team - $($_.Exception.Message)" -ForegroundColor Red
            }
        } else {
            Write-Host "NO URL: $team" -ForegroundColor Yellow
        }
        
        Start-Sleep -Milliseconds 300
    }
}

Write-Host ""
Write-Host "Downloaded: $downloaded/$totalTeams" -ForegroundColor Cyan

# List files
foreach ($league in $teams.Keys) {
    $leagueDir = Join-Path $OutputDir $league
    if (Test-Path $leagueDir) {
        $files = Get-ChildItem $leagueDir -Filter "*.png"
        Write-Host "$league`: $($files.Count) files" -ForegroundColor White
    }
}