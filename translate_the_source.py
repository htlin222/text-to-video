from googletrans import Translator
import os
import re

def translate_to_zh(input_file, output_file):
    with open(input_file) as f:
        lines = f.readlines()

    translated_list = []

    for text in lines:
        translator = Translator()
        translated =translator.translate(text, dest='zh-tw')
        translated_list.append(translated.text)

    with open(output_file, 'w+') as fp:
        for item in translated_list:
            item = remove_unwanted_characters(item)
            fp.write("%s\n" % item)
def remove_unwanted_characters(text):
    text = re.sub('>', '大於', text)
    text = re.sub('<', '小於', text)
    text = re.sub('(\[|\])', '，', text)
    return text

if __name__=='__main__':
    my_file = Path(sys.argv[1])
    if my_file.is_file():
        translate_to_zh(sys.argv[1], sys.argv[2])
        print("Translate Done")
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
