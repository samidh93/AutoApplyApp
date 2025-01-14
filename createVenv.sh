#!/bin/bash

# Set the name of the virtual environment
venv_name="venv"

# Create the virtual environment
python3 -m venv "$venv_name"

chmod +x "$venv_name/bin/activate"
# Activate the virtual environment
source "$venv_name/bin/activate"

#create alis
echo "alias activate='source $venv_name/bin/activate'" >> ~/.bashrc
source ~/.bashrc

#activate
activate
# Install packages from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment (optional)
deactivate
