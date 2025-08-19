@echo off
echo Adding Python to PATH...

set PYTHON_PATH=C:\Users\void7\AppData\Local\Programs\Python\Python312
set PYTHON_SCRIPTS=C:\Users\void7\AppData\Local\Programs\Python\Python312\Scripts

echo Python path: %PYTHON_PATH%
echo Python Scripts path: %PYTHON_SCRIPTS%

REM Add Python to user PATH
setx PATH "%PATH%;%PYTHON_PATH%;%PYTHON_SCRIPTS%"

echo.
echo Python has been added to your PATH!
echo Please restart your command prompt for changes to take effect.
echo.
echo After restarting, you can test with: python --version
