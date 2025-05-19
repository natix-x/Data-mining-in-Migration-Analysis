#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
