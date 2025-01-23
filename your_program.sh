#!/bin/sh
#
# Use this script to run your program LOCALLY.
#
# Note: Changing this script WILL NOT affect how CodeCrafters runs your program.
#
# Learn more: https://codecrafters.io/program-interface

set -e # Exit early if any commands fail

# Copied from .bash_scripts/run.sh
#
# - Edit this to change how your program runs locally
# - Edit .bash_scripts/run.sh to change how your program runs remotely
exec pipenv run python3 -u -m app.main "$@"
