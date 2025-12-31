@echo off
title DemoDream Controller
echo ===================================================
echo   STARTING DEMODREAM BACKEND SYSTEM
echo ===================================================
echo.

:: 1. Start Ollama Model in a separate window
echo [1/2] Launching AI Brain (Ollama)...
start "Ollama Model Service" cmd /k "ollama run gemma3:1b"

:: 2. Wait a moment to ensure terminal opens
timeout /t 2 /nobreak >nul

:: 3. Start Python API Server in this window
echo [2/2] Launching API Server (Uvicorn)...
echo.
echo ---------------------------------------------------
echo  Keep this window OPEN. 
echo  If you see 'Application startup complete', 
echo  the backend is ready!
echo ---------------------------------------------------
echo.

cd Ai_Engine
uvicorn main:app --reload

pause
