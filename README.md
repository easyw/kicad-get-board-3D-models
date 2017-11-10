# kicad-get-board-3D-models

###Very initial release: 
The script can be launched ATM only on win OS


Installing
----------
- Download and unzip the files (*collect3Dmod.bat*, *list_models.py*)
- configure the batch file with yours settings
- run the batch on a **saved** kicad_pcb file

Parameters
----------
- kicad_folder
  (i.e. kicad_folder="C:\Program Files\KiCad")
- kicad_3D_folder 
  (i.e. kicad_3D_folder="C:\Program Files\KiCad\share\kicad\modules\packages3d")
- kicad_version
  (i.e. kicad_version="4" for stable, kicad_version="5" for dev)
- kicad_board
  (i.e. kicad_board="c:\Temp\blinky.kicad_pcb")
- force_update
  (i.e. force_update="/u" to force overwriting local 3D models from github lib; leave it empty to download only missing 3D models)

**NB** if you configure force_update="/u" your old 3D models will get overwrite without confirmation
 
**Hint:** if your kicad 3D models folder is in 'Program' folder, you need to run this batch/script as Administrator


### License
[GNU GENERAL PUBLIC LICENSE v3](https://www.gnu.org/licenses/gpl-3.0.html)
