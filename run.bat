@echo off

start "e-commerce (web APP)" cmd /c python apps/web/app.py
start "e-commerce (api APP)" cmd /c python apps/api/app.py

echo Running... Press any key to stop
pause >nul

taskkill /IM python.exe /F
echo Closed all apps