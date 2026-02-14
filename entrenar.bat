@echo off
echo ========================================
echo   ENTRENAMIENTO CHATBOT CRISTIANO v2.0
echo ========================================
echo.

echo [1/3] Validando datos...
rasa data validate

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Validacion fallida. Revisa los errores arriba.
    pause
    exit /b 1
)

echo.
echo [2/3] Entrenando modelo...
rasa train

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Entrenamiento fallido.
    pause
    exit /b 1
)

echo.
echo [3/3] Entrenamiento completado!
echo.
echo ========================================
echo   SIGUIENTE PASO:
echo   1. Abre una terminal y ejecuta: rasa run actions
echo   2. Abre otra terminal y ejecuta: rasa shell
echo ========================================
echo.
pause
