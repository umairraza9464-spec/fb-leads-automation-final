@echo off
CLS
echo ====================================
echo FB LEADS AUTOMATION - INSTALLER
echo ====================================
echo.
echo Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from python.org
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)
echo Python found!
echo.
echo Installing dependencies...
echo.
pip install selenium requests pillow tkinter --upgrade
echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Edit config.json with your settings
echo 2. Run: python python\enhanced_agent.py
echo 3. Load Chrome extension from extension/ folder
echo.
pause
