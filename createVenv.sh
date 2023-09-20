#!/bin/bash

# Set the name of the virtual environment
venv_name="venv"

# Create the virtual environment
python3 -m venv "$venv_name"

# Activate the virtual environment
source "$venv_name/bin/activate"

# Install packages from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment (optional)
# deactivate
