# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os
import re
import sys
import shutil
import subprocess
from pathlib import Path
import generate_outline_markdown as md
import cleanup
import text_to_speech as tts
import translate_the_source as translate
import pandoc_pptx as pptx
import pptx_to_png as to_png
import export_video
import dictionary


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
    print('\nStart to create the project 🌱🪴 🌴 ')
    create_output_folder(output_folder)
    cleaned_source = output_folder + "/cleaned_" + source
    splitted_source = output_folder + "/splitted_" + source

    # clean first
    cleanup.clean_all(source, cleaned_source)
    # then split
    cleanup.split_all_paragraph(cleaned_source, splitted_source , 600)
    outline_path = output_folder + '/outline.md'
    translated_path = output_folder + '/translated.txt'
    # create outline.md and translated.txt
    md.open_file_then_set_outline(splitted_source, outline_path)
    print('\nStart to translate the source 🇺🇸 ✈️  🇹🇼')
    translate.translate_to_zh(splitted_source, translated_path)
    # create the pptx
    print('\nStart to create slide.pptx 🎁')
    pptx.convert_to_pptx(outline_path, output_folder)
    print('\n✨Done\n')
    # ===== export video or not =====
    answer = input("Do you want to export video? (y/n): ")
    if answer in ('y','yes','ok','OK'):
        export_final(output_folder)
    else:
        print("\nAll right 🤔, will open the folder 📁. ")
        subprocess.run(f"open {output_folder}", shell=True, check=True)

def export_final(output_folder):
    '''
    export again after fixed the error
    '''
    pptx_path = output_folder + '/slide.pptx'
    to_png.convert_pptx_to_image(pptx_path,output_folder)
    translated_path = output_folder + '/translated.txt'
    tts.text_to_speech(translated_path, output_folder)
    export_video.batch_img_and_audio(output_folder)
    export_video.export_final(output_folder)
    print("\n✨Generated pptx, wav, video in the [", output_folder, '] folder')
    print("\n✨Edit translated.txt and slide.pptx in the folder PRN")
    print("\n✨Then run: python main.py", str(my_file) ,"fix\n")
    choice = input("✨Do you want to open the folder? : (y/n) ")
    if choice in ('y','yes'):
        subprocess.run(f"open {output_folder}", shell=True, check=True)
        print("\n✨All done\n")
    else:
        print("\n✨All done\n")
def batch():
    cwd = os.getcwd()
    for file in os.listdir(cwd):
        if file.endswith(".md") or file.endswith(".txt"):
            if not file.endswith("README.md"):
                FILENAME = str(file)
                folder = re.sub(r'\.[A-Za-z]*','', FILENAME)
                print("\nStart generate", FILENAME,"to video")
                project_init(file, folder)

if __name__=='__main__':
    # check if user have input the MODE
    my_file = Path("NotExist.md")
    if len(sys.argv) == 3:
        MODE = str(sys.argv[2])
        my_file = Path(sys.argv[1])
        folder = re.sub(r'\.[A-Za-z]*','',sys.argv[1])
    elif len(sys.argv) ==2:
        MODE = 'init'
        my_file = Path(sys.argv[1])
        folder = re.sub(r'\.[A-Za-z]*','',sys.argv[1])
    else:
        MODE = 'batch'

    # Start to decied whcih MODE will perform
    if my_file.is_file() and MODE == 'init':
        project_init(sys.argv[1], folder)
    elif my_file.is_file() and MODE == 'export':
        print('\nStart 🔧 export video')
        export_final(folder)
        print('\n✨Done! Your vidoe is ready to go.\n')
    elif my_file.is_file() and MODE not in ('init', 'fix'):
        project_init(sys.argv[1], folder)
    elif MODE == ('batch'):
        batch()
    else:
        # If nothing match, will create the file and open the folder for the user
        with open(sys.argv[1], 'w', encoding='UTF-8'):
            print('❌ File not found, will create', my_file, 'for you, your welcome.')
            subprocess.run("open .", shell=True, check=True)
