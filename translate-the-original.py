from googletrans import Translator
import os

with open('original.txt') as f:
    lines = f.readlines()

translated_list = []

for text in lines:
    translator = Translator()
    translated =translator.translate(text, dest='zh-tw')
    translated_list.append(translated.text)
# pc.copy(text1)

with open(r'translated.txt', 'w') as fp:
    for item in translated_list:
        # write each item on a new line
        fp.write("%s\n" % item)
    print('翻譯完成')
