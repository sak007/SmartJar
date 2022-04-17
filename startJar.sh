#!/bin/bash
set -e

echo "Installing requirements"
pip3 install -r requirements.txt

cd code/jar

python3 jar.py
