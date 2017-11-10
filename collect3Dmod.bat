@echo off

echo This script will download or update 3D models of the pcb file from the github repo
echo.

cd %~dp0
SETLOCAL
set kicad_folder="C:\Program Files\KiCad"
:: your KiCad installation folder

set kicad_3D_folder="C:\Program Files\KiCad\share\kicad\modules\packages3d"
:: set kicad_3D_folder="c:\kicad-stable\share\kicad\modules\packages3d"
:: your KiCad 3D models installation folder

set kicad_version="4"
:: KiCad version (4 or 5 for dev release)

set kicad_board="c:\Temp\blinky.kicad_pcb"
:: the kicad_pcb file full path you want to fetch
:: you can also pass this as parameter to the batch file
if %1=="" (echo using internal configured 'kicad_pcb' file) else (set kicad_board=%1)

::set force_update="/u"
:: set force_upd=/u for overwrite old release of 3D models, 
set force_update=
:: set force_update= for download only missing models

::if "%kicad_version%"=="4" (set kicad_lib=%kicad_folder%\share\kicad\modules\packages3d) else (set kicad_lib=%kicad_folder%\share\kicad\modules\packages3d)

echo running on '%kicad_board%'
echo.
%kicad_folder%\bin\python list_models.py %kicad_3D_folder% %kicad_version% %kicad_board% %force_update%

echo.
echo HINT: if your kicad 3D models folder is in 'Program' folder, you need to run this batch as Administrator
echo.

ENDLOCAL

pause