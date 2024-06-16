#!/bin/bash

FILE_NAME="susage"


SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"


FILE_PATH="${SCRIPT_DIR}/${FILE_NAME}.py"

DEST_DIR="/usr/local/bin"


if [ ! -d "$DEST_DIR" ]; then
    exit 1
fi


check_platform() {
    platform=$(uname)
    if [[ "$platform" == "Linux" || "$platform" == "Darwin" ]]; then
        pip3 install curses
    elif [[ "$platform" == "Windows" ]]; then
    else
        exit 1
    fi
}

check_platform
pip install -r "${SCRIPT_DIR}/requirements.txt"


chmod +x "$FILE_PATH"

sudo mv "$FILE_PATH" "$DEST_DIR/$FILE_NAME"

echo "Now you can execute the command: $FILE_NAME"
