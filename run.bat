@echo off
setlocal

REM Navigate to FastAPI backend and run it
cd app
pip install -r requirements.txt
echo Starting FastAPI backend...
start "" /B cmd /C "uvicorn main:app --reload --port 8000"
set "FASTAPI_PID=%!%"

REM Navigate to Vue frontend and run it
cd ../vue
echo Starting Vue frontend...
call npm install
start "" /B cmd /C "npm run dev"
set "VUE_PID=%!%"


echo Waiting for processes... Press Ctrl+C to terminate.
powershell -Command "Register-EngineEvent PowerShell.Exiting -Action { Stop-Process -Name node,python -Force } | Out-Null; while ($true) { Start-Sleep -Seconds 1 }"
