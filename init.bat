@echo off
title Generador de Ejercicios

start /B python app.py

timeout /t 3 /nobreak >nul

start http://localhost:5000

pause >nul

taskkill /F /IM python.exe 2>nul