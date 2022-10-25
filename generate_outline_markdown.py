#!/usr/bin/env python3
# install the packages first
# pip install googletrans==4.0.0-rc1 pyperclip
import re
import sys
import os
from pathlib import Path

def paragraph_to_outlines(text,title_previous):
    '''
    convert paragraph to outline
    '''
    # find if there's title set, if so, replace the old one
    title = find_title(text,title_previous)
    # remove the first line if its used for title
    text = text.replace(title,"")
    # find image
    image = find_image(text)
    # remove image
    text = text.replace(image,"")
    # clean up the citations
    sub_result = clean_citation(text)
    # break the lines English
    sub_result = re.sub('(\s[A-Za-z]*\S[a-z]*[A-Za-z]|]|\%|\)|"|\s)(\.\s\s*)([A-Z][A-Za-z]|A|\d)', '\g<1>.\n\g<3>', sub_result)
    sub_result = re.sub('([\u4e00-\u9fa5\u3000-\u303F])\u3002([\u4e00-\u9fa5\u3000-\u303F])','\g<1>\u3002\n\g<2>', sub_result)

    # Fix the Fig. Number
    sub_result = re.sub('Fig\.\n([0-9]{1,2})','Fig. \g<1>',sub_result)
    # add period if there's no period at the end of line
    sub_result = re.sub('\n\n','.\n',sub_result)
    # delete empty space in the beginning
    sub_result = re.sub('\n\s','\n',sub_result)
    # delete empty line
    sub_result = re.sub('^\n','',sub_result)
    # add '-' in each line and add title
    if title == title_previous:
        sub_result = "## " + title + '(continued)' + "\n\n" + re.sub(r'(?m)^','- ',sub_result)
    else:
        sub_result = "## " + title + "\n\n" + re.sub(r'(?m)^','- ',sub_result)
    result = re.sub(r'(?m)^-\s$', '',sub_result)
    if image != "":
    # if there's image, add to the end
        result = result + "\n" + image + "\n"
    # if no content, then set as title page
    if not re.match('##.*\n\n-\s[^#]', result):
        result = result.replace("##","#")
        result = re.sub(r"\n\n-\s*#","",result)
        print(result)
    return result, title

def read_file(filename):
    '''
    open the file and read the text
    '''
    with open(filename, 'r', encoding='UTF-8') as textfile:
        filetext = textfile.read()
    return filetext

def find_title(text,previous_title):
    titleRegex = re.compile(r'(##*)\s*([\u4e00-\u9fa5A-Za-z].*)\s*(##*|\n)')
    if not re.findall(titleRegex, str(text)) == []:
        title = list(re.findall(titleRegex, str(text))[0])
        return title[1]
    else:
        return previous_title

def find_image(text):
    '''
    find patter matching markdown image style ![]()
    '''
    imageRegex = re.compile(r'!\[.*\]\(.*\)')
    image = re.findall(imageRegex, str(text))
    if not image == []:
        return image[0]
    else:
        return ""

def clean_citation(text):
    # take the ',000' out to avoid been replace
    sub_result = re.sub(',000','KILO',text)
    # move quote inside the period
    sub_result = re.sub('\.("|”)', '".', sub_result)
    # delete the dots at the beginning of the line
    sub_result = re.sub('(●|•)\s*','',sub_result)
    # delete citations: NEJM style, Uptodate style, Clinical Key style
    # 1. NEJM
    sub_result = re.sub(',[0-9]{1,2}', '', sub_result)
    sub_result = re.sub('[0-9]{1,2};', '', sub_result)
    sub_result = re.sub('\.[0-9]{1,2}-[0-9]{1,2}(\s[\u4e00-\u9fa5A-Z][A-Za-z]*|\n)', '.\g<1>', sub_result)
    sub_result = re.sub('\.[0-9]{1,2}(\s[\u4e00-\u9fa5A-Z][A-Za-z]*|$)', '.\g<1>', sub_result)
    # 2. Clinical Key
    sub_result = re.sub('(\.|,|\))\s([0-9]{1,2})(\s|$)([\u4e00-\u9fa5A-Za-z]|A|\d)', '\g<1> \g<3>', sub_result)
    sub_result = re.sub('[0-9]\s\.','.',sub_result)
    # 3. Uptodate
    sub_result = re.sub('\[[0-9]{1,2}\]\.', '. ', sub_result)
    sub_result = re.sub('\[[0-9]{1,2}(-|,)[0-9]{1,2}\]\.', '. ', sub_result)
    # replace KILO back to ,000
    sub_result = re.sub('KILO',',000',sub_result)
    return sub_result

def open_file_then_set_outline(input_file, output_file):
    with open(input_file) as f:
        lines = f.readlines()

    outline_list = []
    default_title = re.sub(r'\.[\u4e00-\u9fa5A-Za-z]*','',input_file)

    for text in lines:
        if not text.isspace():
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
    if my_file.is_file():
        open_file_then_set_outline(sys.argv[1], sys.argv[2])
        print("✨Have generated the", str(sys.argv[1]), 'to', folder)
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
