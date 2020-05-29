import argparse
import os
import random
import sys
from shutil import copy, SameFileError
from pathlib import Path
from glob import glob
from typing import List, Tuple, Union


ExitCode_t = int
THEMES_PATH: str = str(Path('themes/*').resolve())  # Used in main()


def run_argparse() -> argparse.Namespace:
    """ wrap argparse configuration """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c',
        '--copy',
        dest='copy_path',
        help='copy theme to COPY_PATH instead of printint it on the terminal',
    )
    parser.add_argument(
        '-f',
        '--force',
        action='store_true',
        dest='force_copy',
        help='use when with --copy to override file if it already exists',
    )
    theme_selection_group = parser.add_mutually_exclusive_group(required=True)
    theme_selection_group.add_argument(
        '-r', '--random', action='store_true', help='choose a random theme'
    )
    theme_selection_group.add_argument(
        '-t', '--theme', dest='theme_name', help='pass THEME_NAME to choose the theme'
    )
    return parser.parse_args()


def printerr(*args, **kwargs):
    """ print() but to stderr """
    print(*args, file=sys.stderr, **kwargs)


def load_themes(load_path: str) -> Tuple[List[str], List[str]]:
    """
    loads themes from received load_path

    return 2 lists:
        return (paths, names)

    where paths[i] and names[i] correspond to the same theme
    """
    file_paths: List[str] = glob(load_path)

    if not file_paths:
        printerr(f'could not load any themes from {load_path}')
        exit(1)

    # from file_paths, filter the files that are valid themes
    # each tuple is a theme (path, name)
    temp: List[Tuple[str, str]] = [
        (path, first_line[9:-1])
        for path in file_paths
        if (first_line := open(path, 'r').readline()).startswith('# Theme: ')
    ]

    paths: List[str] = [x[0] for x in temp]
    names: List[str] = [x[1] for x in temp]

    return (paths, names)


def basename_sh_util(path: Union[Path, str]) -> str:
    """
    clone of unix's "basename"
    grab a complete path and return only the name of the file (last / forward)
    """
    path: str = str(path)  # turn possible Path type into str type

    # if no /, return it as it is
    if path.find('/') == -1:
        return path
    else:
        return path.rpartition('/')[2]


def copy_theme(
    src: str, dst: str, force_copy_flag: bool, theme_name: str
) -> ExitCode_t:
    """
    --copy COPY_PATH function

    src: source path
    dst: destination path
    force_copy_flag: if dst is already a file, try to overwrite
    theme_name: message at the end that if it was successful
    """

    # resolve the destination path
    dst = str(Path(dst).resolve())

    # if dst is a target directory to where the theme is to be copied to,
    # update the dst to be the final path, and continue checkings for conflicts
    if Path(dst).is_dir():
        dst = dst + '/' + basename_sh_util(src)

    # if new path is also a directory, abort
    if Path(dst).is_dir():
        printerr(f'{dst} is a directory, cannot copy theme to it')
        return 1

    # assert not Path(dst).is_dir()

    # messages
    COPY_SUCCESS_MESSAGE: str = (
        ''
        f'Success! "{theme_name}" theme copied.\n'
        '\n'
        f'from: {src}\n'
        f'to:   {dst}'
    )

    PERMISSION_DENIED_MESSAGE: str = f'Permission denied: {dst}'
    UNEXPECTED_ERROR_MESSAGE: str = '\nA unexpected error occurred :(\n'

    # if destination isn't already a file or is a target directory
    if not Path(dst).exists():
        try:
            copy(src, dst)
        except PermissionError:
            printerr(PERMISSION_DENIED_MESSAGE)
            return 1
        except:
            printerr(UNEXPECTED_ERROR_MESSAGE)
            raise
        # success
        else:
            print(COPY_SUCCESS_MESSAGE)
            return 0

    # assert Path(dst).exists()

    if force_copy_flag is False:
        printerr(f'{dst} file already exists, pass --force to overwrite it')
        return 1

    # assert force_copy_flag is True
    print('--force: trying to replace file')

    if Path(dst).is_file() or Path(dst).is_symlink():

        # tell what you are doing
        if Path(dst).is_file():
            print(f'--force: {dst} is a file, removing')
        if Path(dst).is_symlink():
            print(f'--force: {dst} is a symbolic link, removing')

        try:
            os.remove(dst)
            copy(src, dst)
        except PermissionError:
            printerr(PERMISSION_DENIED_MESSAGE)
            return 1
        except SameFileError:
            printerr("SameFileError: COPY_PATH is the theme source path (why?)")
            return 1
        except:
            printerr(UNEXPECTED_ERROR_MESSAGE)
            raise
        else:
            print(COPY_SUCCESS_MESSAGE)
            return 0


def stdout_theme_output(path: str):
    print(open(path, 'r').read(), end='')


def main():
    """ main function """
    theme_paths: List[str]
    theme_names: List[str]
    theme_paths, theme_names = load_themes(THEMES_PATH)

    args: argparse.Namespace
    args = run_argparse()

    chosen_theme_index: int  # choosing the theme!
    if args.random is True:
        chosen_theme_index = random.randrange(len(theme_paths))

        # check necessary, don't show in case output is meant to be redirected!
        if not args.copy_path:
            print(f'--random chose "{theme_names[chosen_theme_index]}"')

    # picking up theme from chosen
    theme_path = theme_paths[chosen_theme_index]
    theme_name = theme_names[chosen_theme_index]

    if args.copy_path is not None:
        exit(copy_theme(theme_path, args.copy_path, args.force_copy, theme_name))
    else:
        stdout_theme_output(theme_path)


if __name__ == '__main__':
    main()

