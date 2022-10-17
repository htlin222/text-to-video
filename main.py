#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import generate_outline_markdown as md
import text_to_speech as tts
import translate_the_source as translate
import pandoc_pptx as pptx

def create_output_folder(output_folder):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

def project_init(source, output_folder):
    create_output_folder(output_folder)
    outline_path = output_folder + '/' + 'outline.md'
    md.open_file_then_set_outline(source, outline_path)
    pptx.convert_to_pptx(outline_path,output_folder)
    translated_path = output_folder + '/' + 'translated.txt'
    translate.translate_to_zh(source, translated_path)
    tts.text_to_speech(translated_path, output_folder)

if __name__=='__main__':
    my_file = Path(sys.argv[1])
    if my_file.is_file():
        project_init(sys.argv[1], sys.argv[2])
        print("Done ~ ")
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
