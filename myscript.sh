#!/bin/zsh
/Users/balents/anaconda3/bin/python3 scrape-plots-file.py
git add .
git commit -m "update by myscript.sh"
git push origin master


