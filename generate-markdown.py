#!/usr/bin/env python3
# install the packages first
# pip install googletrans==4.0.0-rc1 pyperclip
from googletrans import Translator
import re
import os
import pyperclip as pc
# retrieve the text from the clipboard
text = pc.paste()
def paragraph_to_outlines(text):
    # move quote inside the period
    sub_result = re.sub('\.("|”)', '".', text)
    # delete the dots at the beginning of the line
    sub_result = re.sub('(●|•|•\s)','',sub_result)
    # delete citations: NEJM style, Uptodate style, Clinical Key style
    sub_result = re.sub('([0-9][0-9]*,)', '', sub_result)
    sub_result = re.sub('\.(\d*-\d*)([A-Z][A-Za-z]|A|\d)', '. \g<1>', sub_result)
    sub_result = re.sub('\.\s(\d*)(\s|$)([A-Z][A-Za-z]|A|\d)', '. \g<3>', sub_result)
    sub_result = re.sub('(\.\d*\s|\.\d*$)([A-Z][A-Za-z]|A|\d)', '. \g<2>', sub_result)
    sub_result = re.sub('\[\d.*\d\]\.', '. ', sub_result)
    # break the lines
    sub_result = re.sub('(\s[A-Za-z]*\S[a-z]*[A-Za-z]|]|\%|\)|"|\s)(\.\s\s*)([A-Z][A-Za-z]|A|\d)', '\g<1>.\n\g<3>', sub_result)
    # add period if there's no period at the end of line
    sub_result = re.sub('\n\n','.\n',sub_result)
    # delete empty space in the beginning
    sub_result = re.sub('\n\s','\n',sub_result)
    # delete empty line
    sub_result = re.sub('^\n','',sub_result)
    # add '-' in each line and add title
    result = "# 重點: \n\n" + re.sub(r'(?m)^','- ',sub_result)

with open('original.txt') as f:
    lines = f.readlines()
    # text = lines[0]
# TODO: add for loop for each line
i = 1
for text in lines:
    print(i)
    i = i + 1
