# import ffmpeg
import os
import sys
from pathlib import Path
import subprocess
import re

# subprocess.run(ffmpeg -i ep1.png -i ep1.wav ep1.mp4)
# output_file_path = folder + '/' + 'slide.pptx'
def img_and_audio(input_image,input_audio,output_video):
    '''
    combine an image to wav file to mp4
    '''
    subprocess.run(f"ffmpeg -y -i {input_image} -i {input_audio} -pix_fmt yuv420p {output_video}", shell=True)


def batch_img_and_audio(folder):
    '''
    load files from audio_list.txt
    '''
    i = 1
    the_audio_list = folder + "/" + "audio_list.txt"
    with open(the_audio_list) as the_list:
        lines = the_list.readlines()
    clips_list = []
    for item in lines:
        item = re.sub('\n','',item) # remove the line break
        input_audio = item
        # change to jpg if you want
        input_image = folder + "/slide/" + "投影片" + str(i) + ".png"
        output_video = folder + "/" + "clip" + str(i) + ".mp4"
        if os.path.exists(input_audio):
            img_and_audio(input_image, input_audio, output_video)
        filename = "file " + folder + "/" + "clip" + str(i) + ".mp4"
        filename = "file " + "clip" + str(i) + ".mp4"
        clips_list.append(filename)
        i = i + 1
    clips_txt = folder + '/' + 'concat.txt'
    with open(clips_txt, 'w+') as clips_txt:
        for item in clips_list:
            clips_txt.write("%s\n" % item)
    return clips_txt

#
def export_final(output_folder):
    working_dir = output_folder
    final = str(output_folder) + "_final.mp4"
    subprocess.run(f"ffmpeg -y -f concat -i concat.txt -c copy {final}", cwd=working_dir, shell=True)

def check_folder(output_folder):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        output_folder = input("folder not exists, please enter the correct one: ")

if __name__ == '__main__':
    folder = sys.argv[1]
    check_folder(folder)
    clips_txt = batch_img_and_audio(folder)
    export_final(folder)
    print("\n✨Have generated the combined video in [", folder, "] folder")
