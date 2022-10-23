import os
import re
import main

def generate_all():
    '''
    will do the batch job
    '''
    return 'pending'

if __name__=='__main__':
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".md") or file.endswith(".txt"):
            if not file.endswith("README.md"):
                FILENAME = str(file)
                folder = re.sub(r'\.[A-Za-z]*','', FILENAME)
                main.project_init(file, folder)

    print("\n✨Have generated the all the project\n")
