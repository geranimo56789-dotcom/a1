@echo off
echo 🏆 League 1 Logo Scraper - Working Version
echo ===========================================
echo.
echo Available commands:
echo   list   - Show all available leagues
echo   league  - Download specific league (e.g., France_Ligue1)
echo   all     - Download all leagues
echo.
echo Example: run_working_scraper.bat league France_Ligue1
echo.

if "%1"=="" (
    echo Downloading all leagues...
    .\python.bat league1_scraper_working.py all
) else (
    .\python.bat league1_scraper_working.py %*
)

echo.
echo Done.
