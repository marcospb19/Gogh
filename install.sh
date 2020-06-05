#!/usr/bin/env bash

# Installation of termite-themes

set -e

if [[ ! -d 'themes/' ]]; then
	echo >&2 'themes/ folder not found for installing the themes'
	exit='true'
fi
if [[ ! -f 'termite-themes.py' ]]; then
	echo >&2 'termite-themes.py not found for installation'
	exit='true'
fi
[[ "$exit" == 'true' ]] && exit 1

if [[ "$USER" != 'root' ]]; then
	echo >&2 'Permission denied!'
	exit 1
fi

sudo rm -r /usr/share/termite-themes 2> /dev/null || true
sudo rm /usr/bin/termite-themes      2> /dev/null || true

sudo mkdir /usr/share/termite-themes -p
cp -r themes /usr/share/termite-themes/
cp termite-themes.py /usr/bin/termite-themes
chmod +x /usr/bin/termite-themes


echo "termite-themes installed with success, thanks for using!"
echo "Type \`termite-themes --help\`"
echo ""
echo "Access https://github.com/marcospb19/termite-themes if you want to contribute"
