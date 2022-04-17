#!/bin/bash
set -e

echo "Installing requirements"
pip3 install -r requirements.txt

cd code/bot

python3 bot.py
