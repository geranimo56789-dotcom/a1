@echo off
echo 🏆 Consolidating all logo files into one folder...
echo.

REM Create the consolidated folder
if not exist "all_league_logos" mkdir "all_league_logos"

REM Move all PNG files from subfolders to the main folder
for /r "ultimate_final_logos" %%f in (*.png) do (
    echo Moving: %%~nxf
    move "%%f" "all_league_logos\"
)

echo.
echo ✅ All logos consolidated into: all_league_logos
echo.
pause
