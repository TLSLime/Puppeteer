@echo off
chcp 65001 >nul
title Puppeteer Advanced Options
color 0B

echo.
echo ========================================
echo   Puppeteer Advanced Options
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    echo Please install Python 3.7+ and add it to PATH
    echo.
    pause
    exit /b 1
)

REM 检查文件
if not exist "main.py" (
    echo Error: main.py not found!
    echo Please run this script from the Puppeteer directory
    echo.
    pause
    exit /b 1
)

:menu
echo Please select an option:
echo.
echo 1. GUI Mode (Default)
echo 2. CLI Mode (simple_test config)
echo 3. CLI Mode (example_game config)
echo 4. Run Module Tests
echo 5. Run Demo Program
echo 6. Quick Test
echo 7. Diagnose Problems
echo 8. Exit
echo.
set /p choice="Please enter your choice (1-8): "

if "%choice%"=="1" goto gui
if "%choice%"=="2" goto cli_simple
if "%choice%"=="3" goto cli_example
if "%choice%"=="4" goto tests
if "%choice%"=="5" goto demo
if "%choice%"=="6" goto quick
if "%choice%"=="7" goto diagnose
if "%choice%"=="8" goto exit
echo Invalid choice. Please try again.
echo.
goto menu

:gui
echo.
echo Starting GUI Mode...
echo Note: GUI window will open. Close the window to exit.
echo.
python main.py --mode ui
goto end

:cli_simple
echo.
echo Starting CLI Mode (simple_test)...
echo Note: Press Ctrl+C to stop the automation
echo.
python main.py --mode cli --profile simple_test
goto end

:cli_example
echo.
echo Starting CLI Mode (example_game)...
echo Note: Press Ctrl+C to stop the automation
echo.
python main.py --mode cli --profile example_game
goto end

:tests
echo.
echo Running Module Tests...
echo.
python test_modules.py
goto end

:demo
echo.
echo Running Demo Program...
echo.
python run_demo.py
goto end

:quick
echo.
echo Running Quick Test...
echo.
python quick_test.py
goto end

:diagnose
echo.
echo Running Diagnostics...
echo.
python diagnose.py
goto end

:exit
echo.
echo Exiting...
exit /b 0

:end
echo.
echo ========================================
echo Operation completed. Press any key to continue.
echo ========================================
pause >nul
goto menu
