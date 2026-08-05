@echo off
REM Lanza el bridge del PLC real desde la raiz del repo (donde esta este .bat).
cd /d "%~dp0"

if not exist "plc_bridge.py" (
  echo No encuentro plc_bridge.py en %CD%
  pause
  exit /b 1
)

if not exist "serviceAccountKey.json" (
  echo.
  echo Falta serviceAccountKey.json en:
  echo   %CD%
  echo Pon el JSON de la cuenta de servicio de Firebase ahi.
  echo Ver docs\12_ARCHIVO_NO_ENCONTRADO_WINDOWS.md
  echo.
  pause
  exit /b 1
)

set IP=%~1
if "%IP%"=="" set IP=192.168.0.10

echo CWD=%CD%
echo IP=%IP%
py plc_real\plc_bridge_real.py --ip %IP%
if errorlevel 1 pause
