# termite-themes
Theme manager for termite terminal emulator.

## Requirements:
- Python version >= 3.6

```sh
python --version
```

In some older systems, you may need to type `python3 --version` to receive the desired version, remember this when reading usage!!!!!!

```sh
python3 --version
```

## Features:
There are _187_ themes available (from [Gogh](https://github.com/Mayccoll/Gogh)).

After you choose a theme (by passing `--theme THEME_NAME` or `--random`), you got 2 options:

1. Print the theme content on the terminal
2. Copy it to another `PATH` using `--copy PATH`

Why?

1. You're able to use shell's `>` or `>>` redirection functions to manage your configuration files (see usage).
2. I made a [`fork of termite`](https://github.com/marcospb19/termite) that supports config modularization.

## Installation:
Just clone the repository and enter it
```sh
git clone https://github.com/marcospb19/termite-themes
cd termite-themes
```

## Usage
From within the repository folder, you need to run `termite-themes.py` to manage themes located at `themes/` folder.

How to invoke it:

```sh
python termite-themes.py [options] # Usage format (fake usage)
python termite-themes.py --help    # To see help
```

See the list of themes available:

```sh
python termite-themes.py --list # List all themes
```

How to choose a theme:

```sh
python termite-themes.py --random                # Choose a random theme! (recommended)
python termite-themes.py --theme "Ocean Dark"    # Use "" if theme contains spaces
python termite-themes.py --theme "Vs Code Dark+" #
python termite-themes.py -t "Ocean Dark"         # Shorter version
python termite-themes.py -t "Vs Code Dark+"      #
python termite-themes.py -t Zenburn              # No spaces, "" is optional
python termite-themes.py -t "Zenburn"            #
python termite-themes.py -t 'Zenburn'            # '' works like ""!
```

### Extras:
Vim users, to enable termite files syntax highlight:
> Add `# vim: ft=dosini cms=#%s` your config file
