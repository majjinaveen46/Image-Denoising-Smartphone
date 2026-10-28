@echo off
title NeuroClean Live Studio Launcher
echo =====================================================================
echo           Starting NeuroClean AI Denoising Server & Tunnel
echo =====================================================================
echo.

cd /d "%~dp0"

echo [1/2] Starting FastAPI Backend on port 8000...
start "NeuroClean Backend" cmd /k "python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000"

timeout /t 3 /nobreak >nul

echo [2/2] Starting Cloudflare Public HTTPS Tunnel...
start "Cloudflare Tunnel" cmd /k ""C:\Program Files (x86)\cloudflared\cloudflared.exe" tunnel --url http://127.0.0.1:8000"

echo.
echo =====================================================================
echo  System is running! 
echo  - Local access: http://127.0.0.1:8000
echo  - Public tunnel: Watch the Cloudflare window for your https URL!
echo =====================================================================
