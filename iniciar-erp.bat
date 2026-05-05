@echo off
setlocal

cd /d "%~dp0"

echo ======================================
echo Iniciando ERP Loja de Carros
echo ======================================
echo.

if not exist "python\python.exe" (
    echo ERRO: nao encontrei python\python.exe
    pause
    exit /b 1
)

if not exist "app\manage.py" (
    echo ERRO: nao encontrei app\manage.py
    pause
    exit /b 1
)

echo Testando import do projeto...
python\python.exe -c "import backend; print('Projeto OK')"

if errorlevel 1 (
    echo.
    echo ERRO: o Python nao conseguiu importar o projeto Django.
    echo Confira se python\python313._pth contem a linha:
    echo ..\app
    echo.
    pause
    exit /b 1
)

echo.
echo Aplicando migrations...
cd app
..\python\python.exe manage.py migrate

if errorlevel 1 (
    echo.
    echo ERRO: falha ao aplicar migrations.
    pause
    exit /b 1
)

echo.
echo Abrindo navegador...
start "" "http://127.0.0.1:8000/"

echo.
echo Iniciando servidor...
..\python\python.exe manage.py runserver 127.0.0.1:8000

pause
