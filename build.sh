#!/usr/bin/env bash
# exit on error
set -o errexit

# Install requirements using a specific Python version
python -m pip install --upgrade pip
pip install -r requirements.txt