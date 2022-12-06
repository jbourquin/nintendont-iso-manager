# Authors: Josh Bourquin
# Description: Reformats a directory of GameCube ISO files to match Nintendont's recommended layout.

import os
import re

from argparse import ArgumentParser
from pathlib import Path


GAME_FILE_EXTENSIONS = ['.iso', '.gcm']


def fetch_game_id(game_file_path: Path) -> str:
    """
    Returns the GameID of the specified ISO
    """
    with game_file_path.open('rb') as fp:
        game_id = fp.read(6)

    return game_id.decode('ascii')


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('game_dir', help='Path to the Nintendont game directory')
    args = arg_parser.parse_args()

    # Convert the command line argument to a Path object
    game_dir_path = Path(args.game_dir).resolve()

    # Verify that the directory exists:
    if not game_dir_path.exists():
        raise Exception('The specified path does not exist!')
    
    # Verify that the path object is a directory:
    if not game_dir_path.is_dir():
        return Exception('The specified path is not a directory!')

    # Get a list of game directory's contents
    print(f'Scaning Directory: {game_dir_path.as_posix()}')
    game_dir_content = game_dir_path.glob('*')

    # Iterate through each object to determine if it is a directory or game file
    for item in game_dir_content:

        # Ignore hidden files and directories
        if item.name.startswith('.'):
            continue
        
        # Check to see if the item is a game file directory
        elif item.is_dir():
            
            # Check to see if the directory contains a game.iso file
            game_files = list(item.glob('game.iso'))
            game_file = game_files[0] if game_files else None

            # If the directory contains a game file, make sure the directory name contains the game ID
            if game_file:
                game_title = item.name
                game_id_match = re.match(r"^.*\[(\w{6})\]$", game_title)

                # If the game ID is missing, fetch it from the game file and rename the directory
                if not game_id_match:
                    game_id = fetch_game_id(game_file)
                    old_folder_name = item.resolve().as_posix()
                    new_folder_name = game_dir_path.joinpath(f'{game_title} [{game_id}]').resolve().as_posix()
                    print(f'Renaming Game Folder: {old_folder_name} -> {new_folder_name}')
                    os.rename(old_folder_name, new_folder_name)

        # Check to see if the itme is a game file
        elif item.suffix in GAME_FILE_EXTENSIONS:
            print(f'Found Game File: {item.name}')

            # If the game file is a .gcm, rename it .iso
            if item.suffix == '.gcm':
                new_file_path = item.with_suffix('.iso')
                print(f'Renaming Game File: {item.name} -> {new_file_path.name}')
                item.rename(new_file_path)

            # Fetch the game title
            game_title = item.stem

            # Check to see if the game ID is in the title, if not fetch the game ID from the ISO file
            game_id_match = re.match(r"^.*\[(\w{6})\].iso$", game_title)
            game_id = game_id_match.group(1) if game_id_match else fetch_game_id(item)
            
            # Make a folder for the game
            game_folder = game_dir_path.joinpath(f'{game_title} [{game_id}]')
            print(f'Creating Game Folder: {game_folder.name}')
            game_folder.mkdir(exist_ok=True)

            # Move the game file into the folder and rename it game.iso
            game_iso_path = game_folder.joinpath('game.iso')
            print(f'Moving Game File: {item.name} -> {game_iso_path.relative_to(game_dir_path).as_posix()}')
            item.rename(game_iso_path)


if __name__ == '__main__':
    main()