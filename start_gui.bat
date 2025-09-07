@echo off
chcp 65001 >nul
title Puppeteer GUI
color 0A

echo.
echo ================================
echo        Puppeteer GUI
echo ================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    pause
    exit /b 1
)

REM 检查文件
if not exist "main.py" (
    echo Error: main.py not found!
    pause
    exit /b 1
)

echo Starting GUI Mode...
echo.

python main.py --mode ui

if errorlevel 1 (
    echo.
    echo GUI failed. Press any key to exit.
    pause >nul
) else (
    echo.
    echo GUI completed. Press any key to exit.
    pause >nul
)
