@echo off
rem Abre Brave con el puerto de depuracion 9222 y un perfil propio (Brave ignora el
rem puerto si se usa el perfil por defecto). Puede convivir con tu Brave normal.
rem El perfil vive FUERA del repo, en <carpeta del proyecto>\brave_cdp, y la sesion de
rem TradingView persiste ahi (la primera vez hay que iniciarla a mano en esta ventana).
rem Estructura: <carpeta del proyecto>\repo\tools\abrir_brave_cdp.bat  ->  ..\..\brave_cdp
set "BRAVE=C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
set "PERFIL=%~dp0..\..\brave_cdp"
start "" "%BRAVE%" --remote-debugging-port=9222 --remote-allow-origins=http://127.0.0.1:9222 --user-data-dir="%PERFIL%" "https://www.tradingview.com/chart/"
echo Brave lanzado con el perfil %PERFIL%
echo Comprueba la conexion con:  python tools\cdp_ejecutar.py --listar
