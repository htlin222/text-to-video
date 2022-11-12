# -*- coding: utf-8 -*-
import os
from pathlib import Path
import sys
import subprocess
from yaml import load, SafeLoader

# import pypandoc
# this method not support image link from imgur
# def convert_to_pptx_by_pypandoc(filename, folder):
#
#     output_file_path = folder + '/' + 'slide.pptx'
#     output = pypandoc.convert_file(filename,
#                                 to='pptx',
#                                 outputfile=output_file_path,
#                                 extra_args=['--reference-doc=slidetemp.pptx','--resource-path=/Users/mac/text-to-video']
#                                 )
with open("settings.yaml","r",encoding="UTF-8") as stream:
    settings = load(stream,SafeLoader)
template = settings['slidetemplate']

def convert_to_pptx(filename,folder):
    # pandoc 來源檔.md -o 投影片名.pptx --reference-doc 範本檔.pptx
    subprocess.run(f"pandoc {filename} -o {folder}/slide.pptx --reference-doc {template}", shell=True)

def create_output_folder(output_folder):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

if __name__ == '__main__':
    my_file = Path(sys.argv[1])
    create_output_folder(sys.argv[2])
    if my_file.is_file():
        convert_to_pptx(sys.argv[1], sys.argv[2])
        print("✨Have generated the pptx to", str(sys.argv[2]))
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
