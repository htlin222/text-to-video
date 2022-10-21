#!/usr/bin/env python3
# install the packages first
# pip install googletrans==4.0.0-rc1 pyperclip
import re
import sys
import os
from pathlib import Path

def paragraph_to_outlines(text,title_previous):
    # find if there's title set, if so, replace the old one
    title = find_title(text,title_previous)
    # remove the first line if its used for title
    text = text.replace(title,"")
    # clean up the citations
    sub_result = clean_citation(text)
    # break the lines
    sub_result = re.sub('(\s[A-Za-z]*\S[a-z]*[A-Za-z]|]|\%|\)|"|\s)(\.\s\s*)([A-Z][A-Za-z]|A|\d)', '\g<1>.\n\g<3>', sub_result)
    # Fix the Fig. Number
    sub_result = re.sub('Fig\.\n([0-9]{1,2})','Fig. \g<1>',sub_result)
    # add period if there's no period at the end of line
    sub_result = re.sub('\n\n','.\n',sub_result)
    # delete empty space in the beginning
    sub_result = re.sub('\n\s','\n',sub_result)
    # delete empty line
    final_result = re.sub('^\n','',sub_result)
    # add '-' in each line and add title
    if title == title_previous:
        sub_result = "## " + title + '(continued)' + "\n\n" + re.sub(r'(?m)^','- ',sub_result)
    else:
        sub_result = "## " + title + "\n\n" + re.sub(r'(?m)^','- ',sub_result)
    result = re.sub(r'(?m)^-\s$', '',sub_result)
    print(result)
    return result, title

def read_file(filename):
    textfile = open(filename, 'r')
    filetext = textfile.read()
    return filetext

def find_title(text,previous_title):
    titleRegex = re.compile(r'##\s*([A-Za-z].*)\s*##')
    title = re.findall(titleRegex, str(text))
    if not title == []:
        return title[0]
    else:
        return previous_title

def clean_citation(text):
    # move quote inside the period
    sub_result = re.sub('\.("|”)', '".', text)
    # delete the dots at the beginning of the line
    sub_result = re.sub('(●|•|##*)\s*','',sub_result)
    # delete citations: NEJM style, Uptodate style, Clinical Key style
    # 1. NEJM
    sub_result = re.sub(',[0-9]{1,2}', '', sub_result)
    sub_result = re.sub('[0-9]{1,2};', '', sub_result)
    sub_result = re.sub('\.[0-9]{1,2}-[0-9]{1,2}(\s[A-Z][A-Za-z]*|\n)', '.\g<1>', sub_result)
    sub_result = re.sub('\.[0-9]{1,2}(\s[A-Z][A-Za-z]*|$)', '.\g<1>', sub_result)
    # 2. Clinical Key
    sub_result = re.sub('(\.|,|\))\s([0-9]{1,2})(\s|$)([A-Za-z]|A|\d)', '\g<1> \g<3>', sub_result)
    sub_result = re.sub('[0-9]\s\.','.',sub_result)
    # 3. Uptodate
    sub_result = re.sub('\[[0-9]{1,2}\]\.', '. ', sub_result)
    sub_result = re.sub('\[[0-9]{1,2}(-|,)[0-9]{1,2}\]\.', '. ', sub_result)
    return sub_result

def open_file_then_set_outline(input_file, output_file):
    with open(input_file) as f:
        lines = f.readlines()

    outline_list = []
    default_title = re.sub(r'\.[A-Za-z]*','',input_file)

    for text in lines:
        result = paragraph_to_outlines(text, default_title)
        outline = result[0]
        outline_list.append(outline)
        default_title = result[1]

    with open(output_file, 'w+') as fp:
        for item in outline_list:
            # write each item on a new line
            fp.write("%s\n" % item)

if __name__=='__main__':
    '''
    python generate_outline_markdown.py folder/source.txt
    '''
    my_file = Path(sys.argv[1])
    folder = re.sub(r'/.*','',sys.argv[1])
    if folder == "":
        folder = sys.argv[2]
    if my_file.is_file():
        open_file_then_set_outline(sys.argv[1], folder)
        print("✨Have generated the", str(sys.argv[1]), 'to', folder)
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
