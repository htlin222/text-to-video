#!/usr/bin/env python
import os
from pathlib import Path
import sys
import subprocess
import webbrowser


open_manual = input("Do you want to open online manual? (y/n)")
if open_manual == "y":
    webbrowser.open('https://github.com/htlin222/text-to-video',new=2)

print("Start to import python package, if not installed, will install it")

def check_import_or_install():
    '''
    install all package needed
    '''
    try:
        from googletrans import Translator
    except ImportError as e:
        print(e, 'strat to install')
        subprocess.run(f"pip install googletrans==4.0.0-rc1", shell=True)
    try:
        import azure.cognitiveservices.speech
    except ImportError as e:
        print(e, 'strat to install')
        subprocess.run(f"pip install azure-cognitiveservices-speech", shell=True)
    try:
        import azure.cognitiveservices.speech
    except ImportError as e:
        print(e, 'strat to install')
        subprocess.run(f"pip install azure-cognitiveservices-speech", shell=True)
    try:
        import pypandoc
    except ImportError as e:
        print(e, 'strat to install')
        subprocess.run(f"pip install pypandoc", shell=True)
    try:
        import playsound
    except ImportError as e:
        print(e, 'strat to install')
        subprocess.run(f"pip install playsound", shell=True)
    try:
        import pdf2image
    except ImportError as e:
        print(e, 'strat to install')
        subprocess.run(f"pip install pdf2image", shell=True)
        subprocess.run(f"pip3 install PyObjC", shell=True)
    print("\nAll package installed 🎉\n")
check_import_or_install()

have_homebrew = input("Have you ever installed homebrew? :(y/n)")
if have_homebrew == "y":
    subprocess.run(r"brew install ffmpeg",shell=True)
    subprocess.run(r"brew install pandoc",shell=True)
    subprocess.run(r"brew install --cask libreoffice",shell=True)
    # install Libreoffice
else:
    answer = input("Open the 👁️ webbrowser to install [1️⃣ ffmpeg, 2️⃣ pandoc, and 3️⃣ libreoffice] manually? : (y/n)")
    if answer == "y":
        webbrowser.open('https://github.com/jgm/pandoc/releases/tag/2.19.2',new=2)
        webbrowser.open('https://www.libreoffice.org/download/download-libreoffice/',new=2)
        webbrowser.open('https://evermeet.cx/ffmpeg/',new=2)
        downloaded = input("Have you downloaded all of them? (y/n)")
        if downloaded == "y":
            subprocess.run(f"open ~/Downloads", shell=True)
            subprocess.run(f"open /usr/local/bin", shell=True)
            print("👉Please move ffmpeg into /usr/local/bin")
            print("👉Please run pandoc-2.19.2-macOS.pkg")
            office_installed = input("Is Libreoffice installed?(y/n)")
            if office_installed == "y":
                subprocess.run(f"sudo curl https://gist.githubusercontent.com/pankaj28843/3ad78df6290b5ba931c1/raw/soffice.sh > /usr/local/bin/soffice && sudo chmod +x /usr/local/bin/soffice", shell=True)
                print("Have linked the soffice")
            else:
                print("Please install Libreoffice first.")
        else:
            print("Bye👋")
    else:
        print("Bye👋")

