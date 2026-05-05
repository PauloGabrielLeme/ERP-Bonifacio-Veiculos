@echo off
cd /d "%~dp0\app"

echo Iniciando ERP Loja de Carros...
echo.

start http://127.0.0.1:8000/

..\python\python.exe manage.py runserver 127.0.0.1:8000

pause
