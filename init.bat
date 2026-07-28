@echo off
start /B python app.py
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5000
pause
taskkill /F /IM python.exe >nul 2>&1