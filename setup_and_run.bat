@echo off
setlocal enabledelayedexpansion
title AI Code Review System
color 0A

call :MAIN
echo.
echo Press any key to close...
pause >nul
exit /b

:MAIN
echo ============================================================
echo   AI-Powered Code Review System - Setup and Run
echo ============================================================
echo.

set ROOT=%~dp0
set LOG=%~dp0setup_log.txt
echo Setup started %date% %time% > %LOG%
echo.

echo [STEP 1/8] Checking Python...
python --version >> %LOG% 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python not found!
    echo  Install from: https://www.python.org/downloads/
    echo  IMPORTANT: Tick Add Python to PATH during install.
    exit /b 1
)
python --version
echo  [OK] Python found.
echo.

echo [STEP 2/8] Checking Node.js...
node --version >> %LOG% 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Node.js not found!
    echo  Install from: https://nodejs.org/en/download
    exit /b 1
)
node --version
echo  [OK] Node.js found.
echo.

echo [STEP 3/8] Setting up Python virtual environment...
cd /d %ROOT%
echo  Root dir: %ROOT%
if exist venv\Scripts\activate.bat (
    echo  [SKIP] venv already exists.
) else (
    echo  Creating venv...
    python -m venv venv >> %LOG% 2>&1
    if errorlevel 1 (
        echo  ERROR: Failed to create venv. See setup_log.txt
        exit /b 1
    )
    echo  [OK] venv created.
)
echo.

echo [STEP 4/8] Activating virtual environment...
call %ROOT%venv\Scripts\activate.bat
if errorlevel 1 (
    echo  ERROR: Could not activate venv.
    exit /b 1
)
echo  [OK] Virtual environment active.
echo.

echo [STEP 5/8] Installing PyTorch CPU build...
echo  Large download ~800MB. Please wait...
echo.
pip install torch==2.9.1+cpu torchvision==0.24.1+cpu torchaudio==2.9.1+cpu --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo  Specific version failed. Trying latest CPU build...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    if errorlevel 1 (
        echo  ERROR: Failed to install PyTorch.
        exit /b 1
    )
)
echo  [OK] PyTorch installed.
echo.

echo [STEP 6/8] Installing Python packages...
pip install -r %ROOT%requirements.txt
if errorlevel 1 (
    echo  ERROR: pip install failed. See setup_log.txt
    exit /b 1
)
echo  [OK] Python packages installed.
echo.

echo [STEP 7/8] Installing frontend packages...
cd /d %ROOT%frontend
if exist node_modules (
    echo  [SKIP] node_modules already exists.
) else (
    call npm install
    if errorlevel 1 (
        echo  ERROR: npm install failed.
        cd /d %ROOT%
        exit /b 1
    )
    echo  [OK] Frontend packages installed.
)
cd /d %ROOT%
echo.

if not exist data mkdir data
if not exist data\uploads mkdir data\uploads
if not exist backend\data mkdir backend\data
if not exist backend\data\uploads mkdir backend\data\uploads

echo [STEP 8/8] Starting servers...
echo.
start Backend_Port_8000 cmd /k cd /d %ROOT% ^&^& call venv\Scripts\activate.bat ^&^& cd backend ^&^& uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
echo  [OK] Backend started on port 8000.

timeout /t 5 /nobreak >nul

start Frontend_Port_5173 cmd /k cd /d %ROOT%frontend ^&^& npm run dev
echo  [OK] Frontend started on port 5173.

timeout /t 4 /nobreak >nul
start http://localhost:5173

echo.
echo ============================================================
echo   ALL DONE! App is running.
echo ============================================================
echo.
echo   Frontend  :  http://localhost:5173
echo   Backend   :  http://localhost:8000
echo   API Docs  :  http://localhost:8000/docs
echo.
echo   NOTE: First run downloads the CodeT5 model about 900MB.
echo         Wait for CodeT5 loaded in the backend window.
echo.
echo   To stop: Close the Backend and Frontend windows.
echo ============================================================
exit /b 0
