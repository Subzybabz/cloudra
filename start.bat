@echo off
title CloudRA Startup Script
echo ===================================================
echo   CloudRA - Cloud Migration Risk Assessor
echo ===================================================
echo.
echo [1/3] Activating virtual environment...
if not exist .venv\Scripts\python.exe (
    echo [ERROR] Virtual environment not found. Please run pip install -r requirements.txt first.
    pause
    exit /b
)

echo [2/3] Starting Flask development server in background...
start "CloudRA Server" .venv\Scripts\python -m src.cloud_risk.api

echo [3/3] Waiting for server to initialize...
timeout /t 3 /nobreak > nul

echo Opening dashboard in default web browser...
start "" http://127.0.0.1:5000

echo.
echo Server is running! To stop the server, close the "CloudRA Server" terminal window.
echo.
pause
