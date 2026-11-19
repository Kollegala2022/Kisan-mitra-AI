@echo off
REM KisanMitra AI - Setup and Execution Script for Windows
REM This script automates the installation and running of both backend and frontend

setlocal enabledelayedexpansion

echo ===============================================
echo   KisanMitra AI - Setup and Installation
echo ===============================================
echo.

REM Check prerequisites
echo Checking prerequisites...

python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed. Please install Python 3.9+
    pause
    exit /b 1
)

npm --version >nul 2>&1
if errorlevel 1 (
    echo Error: npm is not installed. Please install Node.js 16+
    pause
    exit /b 1
)

echo OK: Python and npm found
echo.

REM Setup Backend
echo ===============================================
echo Setting up Backend...
echo ===============================================

cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo Warning: Please edit backend\.env and add your Groq API key
    echo    LLM_API_KEY=gsk_your_key_here
)

echo OK: Backend setup complete
echo.

REM Setup Frontend
echo ===============================================
echo Setting up Frontend...
echo ===============================================

cd ..\frontend

echo Installing npm dependencies...
call npm install

echo OK: Frontend setup complete
echo.

REM Print instructions
echo ===============================================
echo   Setup Complete!
echo ===============================================
echo.
echo NEXT STEPS:
echo.
echo 1. Edit backend\.env and add your Groq API key:
echo    LLM_API_KEY=gsk_...
echo.
echo 2. Start Backend Server (in a new terminal):
echo    cd backend
echo    call venv\Scripts\activate.bat
echo    uvicorn app.main:app --reload --port 8000
echo.
echo 3. Start Frontend Dev Server (in another terminal):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open http://localhost:5173 in your browser
echo.
echo Full instructions are in README.md
echo.
pause
