#!/bin/bash

PYTHON_SCRIPT="susage"


SCRIPT_DIR="$(pwd)"


SCRIPT_PATH="$SCRIPT_DIR/$PYTHON_SCRIPT.py"


if [[ ! -f "$SCRIPT_PATH" ]]; then
  echo "Error: The file $SCRIPT_PATH does not exist."
  exit 1
fi


chmod +x "$SCRIPT_PATH"


cat << EOF | sudo tee /usr/local/bin/$PYTHON_SCRIPT
#!/bin/bash
python3 $SCRIPT_PATH "\$@"
EOF


sudo chmod +x /usr/local/bin/$PYTHON_SCRIPT


pip3 show psutil &> /dev/null

if [[ $? -ne 0 ]]; then
  echo "psutil is not installed. Installing..."
  pip3 install psutil
else
  echo "psutil is already installed."
fi

echo "Setup complete. You can now run the script by typing '$PYTHON_SCRIPT' from anywhere in the terminal."
