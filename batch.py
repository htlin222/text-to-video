import os
import re
import sys
from pathlib import Path
import main as main

for file in os.listdir("/mydir"):
    if file.endswith(".txt"):
        print(os.path.join("/mydir", file))

if __name__=='__main__':
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".md") or file.endswith(".txt"):
            folder = re.sub(r'\.[A-Za-z]*','', filename)
            main.project_init(file, folder)
            print("✨Have generated the", folder, "project")
