@echo off
setlocal

cd /d "%~dp0"

echo ======================================
echo Instalador ERP Loja de Carros
echo ======================================
echo.

if not exist "python\python.exe" (
    echo ERRO: python\python.exe nao encontrado.
    pause
    exit /b 1
)

if not exist "python\python313._pth" (
    echo ERRO: python\python313._pth nao encontrado.
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

echo Criando pastas Lib e site-packages no Python portatil...
if not exist "python\Lib" mkdir "python\Lib"
if not exist "python\Lib\site-packages" mkdir "python\Lib\site-packages"

echo.
echo Verificando Python...
python\python.exe --version

if errorlevel 1 (
    echo.
    echo ERRO: python\python.exe nao conseguiu iniciar.
    echo Este script precisa ser executado no Windows.
    pause
    exit /b 1
)

echo.
echo Caminhos que o Python esta enxergando:
python\python.exe -c "import sys; print('\n'.join(sys.path))"

echo.
echo Verificando se pip ja existe...
python\python.exe -c "import pip; print('pip encontrado:', pip.__version__)" >nul 2>nul

if errorlevel 1 (
    echo pip nao encontrado.
    echo Instalando pip dentro de python\Lib\site-packages...
    echo.

    if not exist "get-pip.py" (
        echo ERRO: get-pip.py nao encontrado na raiz do ERP.
        echo Coloque get-pip.py junto de instalar-erp.bat.
        pause
        exit /b 1
    )

    python\python.exe get-pip.py --no-warn-script-location --target=python\Lib\site-packages

    if errorlevel 1 (
        echo.
        echo ERRO: get-pip.py falhou.
        echo Confira se python\python313._pth contem:
        echo python313.zip
        echo .
        echo Lib
        echo Lib\site-packages
        echo import site
        pause
        exit /b 1
    )
) else (
    echo pip ja estava instalado.
)

echo.
echo Testando pip novamente...
python\python.exe -c "import pip; print('pip OK:', pip.__version__)"

if errorlevel 1 (
    echo.
    echo ERRO: pip foi instalado, mas o Python ainda nao consegue importar pip.
    echo O problema provavelmente esta no arquivo python\python313._pth.
    pause
    exit /b 1
)

echo.
echo Instalando dependencias do ERP...
python\python.exe -m pip install --no-warn-script-location --upgrade --target=python\Lib\site-packages -r app\requirements.txt

if errorlevel 1 (
    echo.
    echo ERRO: falha ao instalar dependencias.
    pause
    exit /b 1
)

echo.
echo Verificando Django...
python\python.exe -c "import django; print('Django instalado:', django.get_version())"

if errorlevel 1 (
    echo.
    echo ERRO: Django nao foi encontrado apos a instalacao.
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
echo ======================================
echo Instalacao concluida com sucesso!
echo ======================================
echo.
echo Agora execute iniciar-erp.bat
pause
