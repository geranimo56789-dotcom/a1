@echo off
echo 🏆 Real League Logo Scraper - Unique Team Logos Only
echo ====================================================
echo.
echo Available commands:
echo   list   - Show all available leagues
echo   league  - Download specific league (e.g., Germany_Bundesliga)
echo   all     - Download all leagues
echo.
echo Example: run_real_logos_scraper.bat league Germany_Bundesliga
echo.

if "%1"=="" (
    echo Downloading all leagues...
    .\python.bat league1_scraper_real_logos.py all
) else (
    .\python.bat league1_scraper_real_logos.py %*
)

echo.
echo Done.
