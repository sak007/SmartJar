#!/usr/bin/env bash
set -e

echo "Installing requirements"
pip3 install -r requirements.txt

if [ "$(uname)" == "Darwin" ]; then
  echo "Mac OS detected"
  brew install --cask wkhtmltopdf
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
  echo "Linux detected"
  sudo apt-get install wkhtmltopdf
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
  echo "Windows 32-bit detected"
  echo "Check Readme on How to install wkhtmltopdf"
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
  echo "Windows 64-bit detected"
  echo "Check Readme on How to install wkhtmltopdf"
fi
