@echo off
echo 🏆 Comprehensive League Logo Scraper - All Major Leagues
echo ========================================================
echo.
echo Available commands:
echo   list   - Show all available leagues
echo   league  - Download specific league (e.g., Germany_Bundesliga)
echo   all     - Download all leagues
echo.
echo Example: run_comprehensive_scraper.bat league Germany_Bundesliga
echo.

if "%1"=="" (
    echo Downloading all leagues...
    .\python.bat league1_scraper_comprehensive.py all
) else (
    .\python.bat league1_scraper_comprehensive.py %*
)

echo.
echo Done.
