@echo off
chcp 65001 >nul
title Puppeteer Desktop Automation System
color 0A

echo.
echo ========================================
echo   Puppeteer Desktop Automation System
echo ========================================
echo.

REM 检查Python是否可用
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python not found!
    echo Please install Python 3.7+ and add it to PATH
    echo.
    pause
    exit /b 1
)

REM 检查main.py是否存在
if not exist "main.py" (
    echo Error: main.py not found!
    echo Please run this script from the Puppeteer directory
    echo.
    pause
    exit /b 1
)

REM 默认启动图形界面
echo Starting GUI Mode...
echo Note: GUI window will open. Close the window to exit.
echo.

python main.py --mode ui

REM 检查执行结果
if errorlevel 1 (
    echo.
    echo ========================================
    echo GUI Mode failed. Showing options...
    echo ========================================
    echo.
    echo Please select an alternative mode:
    echo.
    echo 1. Try GUI Mode again
    echo 2. CLI Mode (simple_test config)
    echo 3. CLI Mode (example_game config)
    echo 4. Run Module Tests
    echo 5. Run Demo Program
    echo 6. Quick Test
    echo 7. Test Enhanced Input
    echo 8. Test Advanced Input (Complete)
    echo 9. Test Safety System
    echo 10. Test Window Management
    echo 11. Test Basic Functionality
    echo 12. Install Dependencies
    echo 13. Diagnose Problems
    echo 14. Exit
    echo.
    set /p choice="Please enter your choice (1-14): "
    
    if "%choice%"=="1" (
        echo.
        echo Trying GUI Mode again...
        python main.py --mode ui
    ) else if "%choice%"=="2" (
        echo.
        echo Starting CLI Mode (simple_test)...
        echo Note: Press Ctrl+C to stop the automation
        python main.py --mode cli --profile simple_test
    ) else if "%choice%"=="3" (
        echo.
        echo Starting CLI Mode (example_game)...
        echo Note: Press Ctrl+C to stop the automation
        python main.py --mode cli --profile example_game
    ) else if "%choice%"=="4" (
        echo.
        echo Running Module Tests...
        python test_modules.py
    ) else if "%choice%"=="5" (
        echo.
        echo Running Demo Program...
        python run_demo.py
    ) else if "%choice%"=="6" (
        echo.
        echo Running Quick Test...
        python quick_test.py
    ) else if "%choice%"=="7" (
        echo.
        echo Testing Enhanced Input...
        python test_enhanced_input.py
    ) else if "%choice%"=="8" (
        echo.
        echo Testing Advanced Input (Complete)...
        python test_advanced_input_complete.py
    ) else if "%choice%"=="9" (
        echo.
        echo Testing Safety System...
        python test_safety_system.py
    ) else if "%choice%"=="10" (
        echo.
        echo Testing Window Management...
        python test_window_management.py
    ) else if "%choice%"=="11" (
        echo.
        echo Testing Basic Functionality...
        python test_basic_functionality.py
    ) else if "%choice%"=="12" (
        echo.
        echo Installing Dependencies...
        python install_dependencies.py
    ) else if "%choice%"=="13" (
        echo.
        echo Running Diagnostics...
        python diagnose.py
    ) else if "%choice%"=="14" (
        echo.
        echo Exiting...
        exit /b 0
    ) else (
        echo.
        echo Invalid choice. Exiting...
        exit /b 1
    )
) else (
    echo.
    echo GUI Mode completed successfully.
)

echo.
echo ========================================
echo Program finished. Press any key to exit.
echo ========================================
pause >nul
