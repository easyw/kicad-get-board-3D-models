# kicad-get-board-3D-models

What are for:
------------
These tools will download/update ONLY the 3D models needed by a kicad_pcb board, as defined in the board footprints.
This can be handful when using standard KiCad footprints, that have pre-configured 3D models.

#### Very initial release (not deeply tested): 
The script can be launched ATM only on win OS

Just configure your parameters inside the '*.bat*' file and launch `collect3Dmod.bat`

For Linux or Osx one must use the command line as for example:

`python list_models.py your_kicad_3D_folder 4 your_kicad_board_full_file_path`


Installing
----------
- Download and unzip the files (*collect3Dmod.bat*, *list_models.py*)
- configure the batch file with yours settings
- run the batch on a **saved** kicad_pcb file

Parameters
----------
- kicad_python
  (i.e. kicad_python="C:\Program Files\KiCad\bin\python")
- kicad_3D_folder 
  (i.e. kicad_3D_folder="C:\Program Files\KiCad\share\kicad\modules\packages3d")
- kicad_version
  (i.e. kicad_version="4" for stable, kicad_version="5" for dev)
- kicad_board
  (i.e. kicad_board="c:\Temp\blinky.kicad_pcb")
- force_update
  (i.e. force_update="/u" to force overwriting local 3D models from github lib; leave it empty to download only missing 3D models)
  
'*kicad_pcb*' file can be passed also as parameter (you must use a full file path then) 

**NB** if you configure force_update="/u" your old 3D models will get overwrite without confirmation
 
**Hint:** if your kicad 3D models folder is in 'Program' or '/usr/share/' or '/Library/Application Support/' folder, you need to run this batch/script as Administrator


### License
[GNU GENERAL PUBLIC LICENSE v3](https://www.gnu.org/licenses/gpl-3.0.html)
