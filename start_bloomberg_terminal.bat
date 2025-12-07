@echo off
REM AgentSpoons Bloomberg Terminal Startup Script
REM This script will start the Bloomberg Terminal interface

echo.
echo ================================================================================
echo  AGENTSPOONS BLOOMBERG TERMINAL
echo ================================================================================
echo.

REM Check if Python is available
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.10 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [INFO] Python found:
py --version
echo.

REM Check if required packages are installed
echo [INFO] Checking for required packages...
py -c "import dash, plotly" >nul 2>&1
if errorlevel 1 (
    echo.
    echo [WARNING] Required packages not found. Installing now...
    echo.
    py -m pip install dash plotly dash-bootstrap-components numpy
    if errorlevel 1 (
        echo.
        echo [ERROR] Failed to install packages
        echo Please run manually: py -m pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

echo [OK] All packages installed
echo.

REM Start the Bloomberg Terminal
echo ================================================================================
echo  Starting Bloomberg Terminal...
echo ================================================================================
echo.
echo  URL: http://localhost:8050
echo  Press Ctrl+C to stop the server
echo.
echo ================================================================================
echo.

cd /d "%~dp0"
py src\bloomberg_terminal.py

pause
