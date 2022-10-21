#!/usr/bin/env python3
import os
import re
import sys
import shutil
import pip
from pathlib import Path
import generate_outline_markdown as md
import text_to_speech as tts
import translate_the_source as translate
import pandoc_pptx as pptx


def create_output_folder(output_folder):
    '''
    check if output folder exists, otherwise create it
    '''
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

def project_init(source, output_folder):
    '''
    as follows:
    '''
    # set the folder and file name
    create_output_folder(output_folder)
    source_backup = output_folder + "/" + source
    shutil.copyfile(source, source_backup)
    outline_path = output_folder + '/outline.md'
    translated_path = output_folder + '/translated.txt'
    # create outline.md and translated.txt
    md.open_file_then_set_outline(source, outline_path)
    translate.translate_to_zh(source, translated_path)
    # create the wav files and pptx
    pptx.convert_to_pptx(outline_path, output_folder)
    tts.text_to_speech(translated_path, output_folder)

if __name__=='__main__':
    my_file = Path(sys.argv[1])
    folder = re.sub(r'\.[A-Za-z]*','',sys.argv[1])
    if my_file.is_file():
        project_init(sys.argv[1], folder)
        print("\n✨Have generated pptx and wav files in the [", folder, '] folder')
    else:
        print('❌ please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
