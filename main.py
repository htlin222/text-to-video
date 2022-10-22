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
import pptx_to_png as to_png
import export_video


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
    print('\nStart to creat the project🪴\n')
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
    # ===== fix =====
    # convert pptx to slide in slide folder
    fix(output_folder)

def fix(output_folder):
    '''
    export again after fixed the error
    '''
    pptx_path = output_folder + '/slide.pptx'
    to_png.convert_pptx_to_image(pptx_path,output_folder)
    translated_path = output_folder + '/translated.txt'
    tts.text_to_speech(translated_path, output_folder)
    export_video.batch_img_and_audio(output_folder)
    export_video.export_final(output_folder)

if __name__=='__main__':
    my_file = Path(sys.argv[1])
    folder = re.sub(r'\.[A-Za-z]*','',sys.argv[1])
    mode = str(sys.argv[2])
    if my_file.is_file() and mode == 'init':
        project_init(sys.argv[1], folder)
        print("\n✨Generated pptx, wav, video in the [", folder, '] folder')
        print("\nEdit translated.txt and slide.pptx in the folder PRN")
        print("\nThen run: python main.py PORJECT.md fix\n")
    elif my_file.is_file() and mode == 'fix':
        print('\nStart 🔧 export again')
        fix(folder)
        print('\n✨Fixed ! \n')

    else:
        print('❌ please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
