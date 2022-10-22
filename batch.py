import os
import re
import sys
from pathlib import Path
import main as main


if __name__=='__main__':
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".md") or file.endswith(".txt"):
            if not file.endswith("README.md"):
                filename = str(file)
                folder = re.sub(r'\.[A-Za-z]*','', filename)
                main.project_init(file, folder)
                print("\n✨Have generated the", folder, "project\n")
