@echo off
echo Searching for Python installation...

REM Check common Python locations
if exist "C:\Python*\python.exe" (
    for /d %%i in (C:\Python*) do (
        if exist "%%i\python.exe" (
            echo Found Python at: %%i
            set PYTHON_PATH=%%i
            goto :found
        )
    )
)

if exist "%LOCALAPPDATA%\Programs\Python*\python.exe" (
    for /d %%i in ("%LOCALAPPDATA%\Programs\Python*") do (
        if exist "%%i\python.exe" (
            echo Found Python at: %%i
            set PYTHON_PATH=%%i
            goto :found
        )
    )
)

if exist "C:\Program Files\Python*\python.exe" (
    for /d %%i in ("C:\Program Files\Python*") do (
        if exist "%%i\python.exe" (
            echo Found Python at: %%i
            set PYTHON_PATH=%%i
            goto :found
        )
    )
)

echo Python not found in common locations.
echo Please manually add your Python installation directory to PATH.
echo You can do this by:
echo 1. Press Win+R, type "sysdm.cpl" and press Enter
echo 2. Go to Advanced tab, click "Environment Variables"
echo 3. Under "User variables", find "Path" and click "Edit"
echo 4. Click "New" and add your Python directory path
echo 5. Click OK on all dialogs
pause
exit /b 1

:found
echo.
echo To add Python to PATH, run this command as Administrator:
echo setx PATH "%%PATH%%;%PYTHON_PATH%"
echo.
echo Or manually add this path to your system PATH:
echo %PYTHON_PATH%
echo.
echo After adding to PATH, restart your command prompt.
pause
