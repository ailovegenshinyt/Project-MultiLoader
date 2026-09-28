@echo off

:: Check for administrative permissions and self-elevate
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"

if '%errorlevel%' NEQ '0' (
    goto UACPrompt
) else (
    goto gotAdmin
)

:UACPrompt
echo Set UAC = CreateObject("Shell.Application") > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
del "%temp%\getadmin.vbs"
exit /B

:gotAdmin
echo Running as Administrator...
timeout /t 1

cls
echo.
echo  Project-MultiLoader
echo.
echo  [1] Run in Local Mode
echo  [2] Run with Ngrok Mode
echo.

:choice
set /p "MODE=Select mode (1 or 2): "

cls

setlocal enabledelayedexpansion

:: Define the target port
set "TARGET_PORT=8080"

echo Searching for processes listening on port %TARGET_PORT%...

:: Kill any process already on port 8080
for /f "tokens=5" %%P in ('netstat -ano ^| findstr /R /C:":%TARGET_PORT% .*LISTENING"') do (
    echo Found PID %%P listening on port %TARGET_PORT%.
    taskkill /PID %%P /F
    set "FOUND=1"
)

if not defined FOUND (
    echo No active process found listening on port %TARGET_PORT%.
)

timeout /t 2

color 2
cls

set "PY_CMD={{PYTHON_EXE}}"
if "!PY_CMD!"=="" set "PY_CMD=python"
if "!PY_CMD!"=="{{PYTHON_EXE}}" set "PY_CMD=python"

if "%MODE%"=="1" (
    cls
    echo Starting in [LOCAL MODE]...
    cd /d "{{INSTALL_DIR}}"
    (echo 1) | "!PY_CMD!" app.py
    goto end
)

if "%MODE%"=="2" (
    cls
    echo Starting in [NGROK MODE]...
    cd /d "{{INSTALL_DIR}}"
    (echo 2& echo.& echo.) | "!PY_CMD!" app.py
    goto end
)

echo Invalid choice, please press 1 or 2.
goto choice

:end
