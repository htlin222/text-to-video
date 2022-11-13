# -*- coding: utf-8 -*-
#!/usr/bin/env python3
import os, re, sys, shutil, subprocess, platform

def create_output_folder(output_folder):
    '''
    check if output folder exists, otherwise create it
    '''
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

def create_settings():
    '''
    create settings.yaml if not exist
    '''
    path_settings = 'settings.yaml'
    try:
        with open(path_settings,'r', encoding='UTF-8') as f_settings:
            print("settings.yaml exists")
    except IOError:
        write_settings()
        sys.exit()

def write_settings():
    '''
    create the settings.yaml and write default settings
    '''
    filepath = "settings.yaml"
    with open(filepath,'w+') as default_settings:
        default_settings.write('subscription: "YOURKEY"\n')
        default_settings.write('region: "southeastasia"\n')
        default_settings.write('slidetemplate: "slidetemp.pptx"\n')
        default_settings.write('openclip: "openclip.mp4"\n')
        default_settings.write('closeclip: "closeclip.mp4"\n')
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filepath))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filepath)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filepath))
    print("Created settings.yaml, please edit the apikeys, Byebye")
