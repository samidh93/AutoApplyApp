#!/bin/bash


# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment
source "venv/bin/activate"

# Install packages from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment (optional)
#deactivate
