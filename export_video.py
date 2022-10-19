import ffmpeg
import os
from pathlib import Path
import subprocess

# subprocess.run(ffmpeg -i ep1.png -i ep1.wav ep1.mp4)
# output_file_path = folder + '/' + 'slide.pptx'
def img_and_audio(input_image,input_audio):
    (
        ffmpeg
        .concat(input_image, input_audio, v=1, a=1)
        .output(output_video)
        .run(overwrite_output=True)
    )

def batch_img_and_audio(folder):
    i = 1
    the_audio_list = folder + "/" + "audio_list.txt"
    with open(the_audio_list) as the_list:
        lines = the_list.readlines()
    for item in lines:
        input_audio = folder + "/" + item
        input_image = folder + "/slides/" + "投影片" + str(i) + ".png"
        if os.path.exists(input_image):
            img_and_audio(input_image, input_audio, folder)
        i = i + 1
    the_clips_list = 'concat.txt'
    with open(output_file, 'w+') as fp:
        for item in the_clips_list:
            item = remove_unwanted_characters(item)
            fp.write("%s\n" % item)
    return the_clips_list

#
def export_final(the_clips_list, output_folder):
    final_path =  output_folder + "/" + "final.mp4"
    subprocess.run(f"ffmpeg -f concat -i concat.txt -c copy  {final_path}", shell=True)

def check_folder(output_folder):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        output_folder = input("folder not exists, please enter the correct one: ")


if __name__ == '__main__':
    folder = sys.argv[1]
    the_clips_list = batch_img_and_audio(folder)
    export_final(the_clips_list,folder)
    print("✨Have generated the final vidoe in", folder)
