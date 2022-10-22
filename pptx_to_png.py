import re
import os
import sys
import re
from pathlib import Path
import subprocess
from pdf2image import convert_from_path

def convert_pptx_to_image(pptx_file, folder):
    '''
    user soffice commandline tool and pdf2image
    '''
    pptx_path = pptx_file
    soffice_command = 'soffice --headless --invisible --convert-to pdf --outdir'
    subprocess.run(f'{soffice_command} {folder} {pptx_path}', shell=True)
    pdf_path = folder + '/slide.pdf'
    images = convert_from_path(pdf_path)
    slide_folder = folder + '/slide'
    if not os.path.exists(slide_folder):
        os.makedirs(slide_folder)
    for i in range(len(images)):
        images[i].save(slide_folder + '/投影片' + str(i+1) + '.png', 'PNG')
        print('saved 💾 : ', slide_folder + '/投影片' + str(i+1) + '.png')

if __name__=='__main__':
    pptx = Path(sys.argv[1])
    if pptx.is_file():
        convert_pptx_to_image(sys.argv[1],sys.argv[2])
        final_folder = str(sys.argv[2]) + '/slide'
        print("\n✨Have converted 🔄 slide.pptx to 投影片.png in ", final_folder ,"folder\n")
    else:
        print("file not found 😢 ")
