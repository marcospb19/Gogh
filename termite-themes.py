import argparse
import sys
from pathlib import Path
from glob import glob
from typing import List, Tuple


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


def load_themes(path: str) -> Tuple[List[str], List[str]]:
    """
    loads themes from received path

    returns 2 lists:
       return (paths, names)

    where paths[i] and names[i] correspond to information from same theme
    """
    file_paths: List[str] = glob(path)

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


def main():
    """ main function """
    theme_paths: List[str]
    theme_names: List[str]
    theme_paths, theme_names = load_themes(THEMES_PATH)

    args: argparse.Namespace
    args = run_argparse()


if __name__ == '__main__':
    main()

