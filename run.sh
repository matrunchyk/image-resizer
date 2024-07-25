#!/bin/bash

# Define the virtual environment directory and main scripts
VENV_DIR=venv
GUI_SCRIPT=gui.py
CLI_SCRIPT=cli.py

# Install prerequisites for tkinter
echo "Checking and installing prerequisites for tkinter..."

# Check if Homebrew is installed
if ! command -v brew &> /dev/null
then
    echo "Homebrew could not be found, installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Python-tkinter via Homebrew
brew install python@3.12
brew link --overwrite python@3.12
brew install tcl-tk
brew install python-tk

# Set environment variables for tcl-tk
export PATH="/usr/local/opt/tcl-tk/bin:$PATH"
export LDFLAGS="-L/usr/local/opt/tcl-tk/lib"
export CPPFLAGS="-I/usr/local/opt/tcl-tk/include"
export PKG_CONFIG_PATH="/usr/local/opt/tcl-tk/lib/pkgconfig"

# Create a virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv $VENV_DIR
fi

# Activate the virtual environment
source $VENV_DIR/bin/activate

# Install the required packages
echo "Installing packages..."
pip install -r requirements.txt

# Check for --cli argument
if [ "$1" == "--cli" ]; then
    echo "Running the CLI script..."
    python $CLI_SCRIPT
else
    echo "Running the GUI script..."
    python $GUI_SCRIPT
fi

# Deactivate the virtual environment
deactivate

