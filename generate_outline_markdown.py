#!/usr/bin/env python3
# install the packages first
# pip install googletrans==4.0.0-rc1 pyperclip
import re
import sys
import os
from pathlib import Path

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
    sub_result = "## 重點: \n\n" + re.sub(r'(?m)^','- ',sub_result)
    result = re.sub(r'(?m)^-\s$', '',sub_result)
    print(result)
    return result

def read_file(filename):
    textfile = open(filename, 'r')
    filetext = textfile.read()
    return filetext

def open_file_then_set_outline(input_file, output_file):
    with open(input_file) as f:
        lines = f.readlines()

    outline_list = []

    for text in lines:
        outlines = paragraph_to_outlines(text)
        outline_list.append(outlines)

    with open(output_file, 'w+') as fp:
        for item in outline_list:
            # write each item on a new line
            fp.write("%s\n" % item)

if __name__=='__main__':
    my_file = Path(sys.argv[1])
    if my_file.is_file():
        open_file_then_set_outline(sys.argv[1], sys.argv[2])
        print("✨Have generated the", str(sys.argv[1]), 'to', str(sys.argv[2]))
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
