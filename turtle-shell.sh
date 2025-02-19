#!/bin/sh
#
# Use this script to run your program LOCALLY.


set -e # Exit early if any commands fail

# Copied from .bash_scripts/run.sh
#
# - Edit this to change how your program runs locally
# - Edit .bash_scripts/run.sh to change how your program runs remotely
exec python -m venv turtle-venv
exec source turtle-venv/bin/activate
exec pip install --upgrade pip
exec pip install -r requirement.txt
exec python app/main.py
