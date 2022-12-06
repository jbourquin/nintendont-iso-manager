# nintendont-toolbox

Collection of Python scripts for managing Nintendont game files.

## repair_game_dir.py

Python script that scans a specified directory for GameCube ISO files and reformats them to match Nintendont's recommended layout. 

This script performs the following actions:

1. Open each ISO and retrive the GameID
2. Create a separate folder for each game named: `<GameTitle> [<GameID>]`
3. Rename the ISO file to `game.iso`
4. Move the `game.iso` file into the newly created directory

Reformating the ISO files in this manner will allow them to work with USB loaders such as USB Loader GX.
