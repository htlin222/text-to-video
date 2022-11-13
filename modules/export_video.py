# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path
import subprocess
import re
import shutil
import soundfile as sf
from yaml import load, SafeLoader

# output_file_path = folder + '/' + 'slide.pptx'
def img_and_audio(input_image,input_audio,output_video):
    '''
    combine an image to wav file to mp4 according to wav duration, which calculated by frames devided by samplerate
    '''
    audio = sf.SoundFile(input_audio)
    duration = audio.frames / audio.samplerate
    settings = "-c:v libx264 -tune stillimage -c:a aac -b:a 96k -r 30 -pix_fmt yuv420p -t " + str(duration)
    subprocess.run(f"ffmpeg -y -loop 1 -i {input_image} -i {input_audio} {settings} {output_video}", shell=True)
    print("❇️  \n\n📺 Have combined", input_image, "and", output_video, "together\n\n❇️  ")

def batch_img_and_audio(folder):
    '''
    load files from audio_list.txt
    '''
    i = 1
    # read the audio_list from txt files and import them into a list
    the_audio_list = os.path.join(folder, "audio_list.txt")
    with open(the_audio_list) as the_list:
        lines = the_list.readlines()
    clips_list = []
    for item in lines:
        item = re.sub('\n','',item) # remove the line break
        input_audio = item
        # if your export image as .jpg, them change the .png to it
        input_image = folder + "/slide/" + "投影片" + str(i) + ".png"
        slide_with_number = "投影片" + str(i) + ".png"
        input_image = os.path.join(folder,"slide",slide_with_number)
        output_video = folder + "/" + "clip" + str(i) + ".mp4"
        clip_with_number = "clip" + str(i) + ".mp4"
        output_video = os.path.join(folder,clip_with_number)
        if os.path.exists(input_audio):
            img_and_audio(input_image, input_audio, output_video)
        # create the clip list
        filename = "file " + "clip" + str(i) + ".mp4"
        clips_list.append(filename)
        if os.path.isfile(input_audio):
            os.remove(input_audio)
        if os.path.isfile(input_image):
            os.remove(input_image)
        i = i + 1
    # write clips_list into concat.txt, which will be used later for combine into one video
    clips_txt = os.path.join(folder,'concat.txt')
    # if there's open title, then add opentitle to the concat list
    with open(clips_txt, 'w+') as clips_txt:
        # add_open_end_in_concat("openclip",clips_txt):
        for item in clips_list:
            clips_txt.write("%s\n" % item)
        # add_open_end_in_concat("closeclip",clips_txt):

def add_open_end_in_concat(otherclip,clips_txt):
    '''
    if there's file name openclip in the project folder, then add it to the concat.txt
    '''
    with open("settings.yaml","r",encoding="UTF-8") as settings_file:
        settings = load(settings_file,SafeLoader)
        my_clip = settings[otherclip]
        if os.path.isfile(my_clip):
            # copy open clip here
            shutil.copy(my_clip, folder)
            filename = "file " + my_clip
            clips_txt.write("%s\n" % filename)
#
def export_final(output_folder):
    working_dir = output_folder
    final = str(output_folder) + "_final.mp4" # like demo_final.mp4
    subprocess.run(f"ffmpeg -y -err_detect ignore_err -f concat -safe 0 -i concat.txt -c:v libx264 -c copy {final}", cwd=working_dir, shell=True)
# -pix_fmt yuv420p
    delete_clips_audio_slide(output_folder)
    print("Delete all the temp files")


# Delete all the unused files
def delete_clips_audio_slide(output_folder):
    full_path_of_concat = os.path.join(output_folder, "concat.txt")
    full_path_of_audio = os.path.join(output_folder, "audio_list.txt")
    slide_path_folder = os.path.join(output_folder,"slide")
    with open(full_path_of_concat) as f:
        clips_count = len(f.readlines())
        for i in range(1, clips_count+1):
            clip_name =  "clip" + str(i) + ".mp4"
            clip_path = os.path.join(output_folder,clip_name)
            if os.path.isfile(clip_path):
                os.remove(clip_path)
    if os.path.isfile(full_path_of_audio):
        os.remove(full_path_of_audio)
    if os.path.isfile(full_path_of_concat):
        os.remove(full_path_of_concat)
    if os.path.isdir(slide_path_folder):
        shutil.rmtree(slide_path_folder)

def check_folder(output_folder):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        output_folder = input("folder not exists, please enter the correct one: ")

if __name__ == '__main__':
    folder = sys.argv[1]
    check_folder(folder)
    batch_img_and_audio(folder)
    export_final(folder)
    print("\n✨Have generated the combined video in [", folder, "] folder")
