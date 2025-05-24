#!/bin/sh
#
# Use this script to run your program LOCALLY.


set -e # Exit early if any commands fail

#
# - Edit this to change how your program runs locally
# - Edit .bash_scripts/run.sh to change how your program runs remotely
python -m venv .venv
echo _____________________________________________________________________
echo virtual enviroment setup named ".venv"
echo _____________________________________________________________________
. turtle-venv/bin/activate
echo _____________________________________________________________________
echo virtual enviroment activated
echo _____________________________________________________________________
pip install --upgrade pip
echo _____________________________________________________________________
echo pip upgraded
echo _____________________________________________________________________
pip install -r requirement.txt
echo _____________________________________________________________________
echo dependancies installed....running the program now
echo _____________________________________________________________________
exec python app/main.py
