@echo off
echo 🏆 Ultimate Final League Logo Scraper - All 13 Countries
echo ========================================================
echo.
echo Available commands:
echo   list   - Show all available leagues
echo   league  - Download specific league (e.g., Germany_Bundesliga)
echo   all     - Download all leagues
echo.
echo Example: run_ultimate_final_scraper.bat league Germany_Bundesliga
echo.

if "%1"=="" (
    echo Downloading all leagues...
    .\python.bat league1_scraper_ultimate_final.py all
) else (
    .\python.bat league1_scraper_ultimate_final.py %*
)

echo.
echo Done.
