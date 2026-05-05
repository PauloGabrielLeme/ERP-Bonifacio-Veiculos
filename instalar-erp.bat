@echo off
cd /d "%~dp0"

echo ======================================
echo Instalando dependencias do ERP...
echo ======================================
echo.

if not exist "python\python.exe" (
    echo ERRO: python\python.exe nao encontrado.
    pause
    exit /b 1
)

if not exist "app\manage.py" (
    echo ERRO: app\manage.py nao encontrado.
    pause
    exit /b 1
)

if not exist "app\requirements.txt" (
    echo ERRO: app\requirements.txt nao encontrado.
    pause
    exit /b 1
)

if not exist "python\Lib" (
    mkdir "python\Lib"
)

if not exist "python\Lib\site-packages" (
    mkdir "python\Lib\site-packages"
)

echo.
echo Verificando pip...
python\python.exe -m pip --version >nul 2>nul

if errorlevel 1 (
    echo pip nao encontrado. Instalando pip...

    if not exist "get-pip.py" (
        echo ERRO: get-pip.py nao encontrado.
        echo Coloque o get-pip.py na raiz do ERP ou baixe novamente.
        pause
        exit /b 1
    )

    python\python.exe get-pip.py

    if errorlevel 1 (
        echo ERRO: falha ao instalar pip.
        pause
        exit /b 1
    )
)

echo.
echo Instalando dependencias...
python\python.exe -m pip install -r app\requirements.txt

if errorlevel 1 (
    echo ERRO: falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo Aplicando migrations...
cd app
..\python\python.exe manage.py migrate

if errorlevel 1 (
    echo ERRO: falha ao aplicar migrations.
    pause
    exit /b 1
)

echo.
echo Instalacao concluida com sucesso.
echo Execute iniciar_erp.bat para abrir o sistema.
pause
