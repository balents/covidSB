#!/bin/zsh
python3 scrape-plots-file.py
git add .
git commit -m "update by myscript.sh"
git push origin master


