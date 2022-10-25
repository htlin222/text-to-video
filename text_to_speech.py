import os
import re
import sys
from pathlib import Path
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechSynthesizer
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# def text_to_speech(input_file):
# export SPEECH_KEY and SPEECH_REGION in your zshrc or zprofile
speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

SSML_SETTINGS = '<voice name="zh-TW-YunJheNeural"><prosody rate="15%" pitch="+5%">'
SSML_START = '<speak xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xmlns:emo="http://www.w3.org/2009/10/emotionml" version="1.0" xml:lang="en-US">'
SSML_END = '</prosody></voice></speak>'
# Test the voice: https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/#features
# <voice name="zh-TW-YunJheNeural"><prosody rate="24%" pitch="-10%"> 基本元素 </prosody></voice>
def text_to_speech(input_file,output_folder):
    with open(input_file) as f:
        lines = f.readlines()
    i = 1
    audio_list = []
    for text in lines:
        ssml = SSML_START + SSML_SETTINGS + text + SSML_END
        result = synthesizer.speak_ssml_async(ssml).get()
        stream = AudioDataStream(result)
        filename = output_folder + "/" + str(i) + '_voice' + '.wav'
        filename = re.sub('\n.wav','.wav',filename)
        stream.save_to_wav_file(filename)
        print("saved 💾", filename)
        audio_list.append(filename)
        i = i + 1
    audio_list_file = output_folder + '/' + "audio_list.txt"
    with open(audio_list_file, 'w+') as fp:
        for item in audio_list:
            fp.write("%s\n" % item)

if __name__=='__main__':
    '''
    python text_to_speech.py folder/translated.txt
    '''
    my_file = Path(sys.argv[1])
    folder = re.sub(r'/.*','',sys.argv[1])
    if folder == "":
        folder = sys.argv[2]
    if my_file.is_file():
        text_to_speech(sys.argv[1], folder)
        print("Done")
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
