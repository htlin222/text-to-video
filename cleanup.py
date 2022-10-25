#!/usr/bin/env python3
import re
import sys
import os
from pathlib import Path
import generate_outline_markdown as md

input_file = 'break.md'
output_file = 'done_break.md'

def split_single_paragraph(paragraph):
    sentenceEnders = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
          (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        \s+               # Split on whitespace between sentences.
        """,
        re.IGNORECASE | re.VERBOSE)
    sentenceList = sentenceEnders.split(paragraph)
    return sentenceList

def split_all_paragraph(input_file,output_file,page_max):
    '''
    read file line by line, check if line too long, split it ~
    '''

    with open(input_file) as f:
        lines = f.readlines()

    main =[] # for the output_file
    # page_max = 800 # if any paragraph longer than this number

    for paragraph in lines:
        # if the paragraph is very long, then break it
        paragraph = md.clean_citation(paragraph)
        if not paragraph.isspace() and len(paragraph) > page_max:
            # split the paragraph into individual lines
            sentenceList = split_single_paragraph(paragraph)
            whole_lengh = 0
            current_page = ""
            for line in sentenceList:
                # conitnue append the current_page
                if whole_lengh + len(line) < page_max and line !=sentenceList[-1]:
                    current_page = current_page + line + " "
                    whole_lengh = whole_lengh + len(line)
                elif line == sentenceList[-1]:
                    current_page = current_page + line + "\n"
                    main.append(current_page)
                else:
                    main.append(current_page)
                    current_page = line + " "
                    whole_lengh = 0

        elif not paragraph.isspace():
            main.append(paragraph)

    with open(output_file, 'w+') as fp:
        for item in main:
            # write each item on a new line
            fp.write("%s\n" % item)

def clean_uptodate(input_file):
    '''
    search pattern in uptodate and clean up
    '''
    with open(input_file, 'r') as file:
        full_text = file.read()
    # Remove the context below the title
    output_file = re.sub(r'\..*','',input_file) + "_cleaned.md"
    result = full_text
    ###### Start the regex
    result = re.sub(r'(#\s(.*)- UpToDate)\n((.*\n)*)(INTRODUCTION)',"\g<1>\n\nINTRODUCTION",result)
    result = re.sub(r'\(chrome[^\)]*\)','',result)
    # 1st level of title
    result = re.sub(r'(([A-Z][A-Z]*\s)([A-Z][A-Z]*\s)*)(—\s|\n)','\n# \g<1>\n\n',result)
    result = re.sub(r'','',result)
    # 2nd level of title
    result = re.sub('(([A-Z][a-z]*(/|\s))([a-z][a-z]*(/|\s))*)—\s*','## \g<1>\n ',result)
    # 3rd level of title
    result = re.sub(r'^(.*)\s—','## \g<1>\n',result)
    # ponit combine to one paragraph
    result = re.sub(r'(●|•)([A-Z]([a-z]*\s)*([a-z]*)[\S])\n\n','\g<2>. ', result)
    result = re.sub(r'\n(([A-Z][a-z][a-z]*)(\s[a-z]*)*\n)','\n## \g<1>',result)
    result = re.sub(r'(●|•)((\*\*(([A-Za-z][a-z]*)(\s[a-z]*)*)\*\*).*)\s–\s','## \g<2> \n',result)
#
    # One line by stars
    result = re.sub(r'\n(●|•)((\*\*(([A-Za-z][a-z]*)(\s[a-z]*)*)\*\*).*[^–])\n','\n## \g<2>\n',result)
    result = re.sub(r'(\\\[|\\\])','',result)
    result = re.sub(r'(\[[0-9]{1,2}((-|,)[0-9]{1,2})*\])','',result)
    result = re.sub(r'\[("|\')(.*)("|\')\]','"\g<2>"',result)
    result = re.sub(r'<(/*)sup>','',result)
    result = re.sub(r'\[([A-Za-z][a-z]*)\]','\g<1>',result)
    result = re.sub(r'(●|—\s*|•)','',result)
    result = re.sub(r'\[inbox\]','',result)
    result = re.sub(r'\*\*','',result)
    with open(output_file, 'w+') as fp:
        fp.write(result)
    print(result)

    print("\n🥟 Uptodate is clear")

def clean_nejm(input_file):
    with open(input_file, 'r') as file:
        full_text = file.read()
    output_file = re.sub(r'\..*','',input_file) + "_cleaned.md"
    result = full_text
    ### Regex Start

    with open(output_file, 'w+') as fp:
        fp.write(result)
    print(result)

    print("\n🥟 NEJM is clear")

def clean_clinicalkey(input_file):
    with open(input_file, 'r') as file:
        full_text = file.read()
    output_file = re.sub(r'\..*','',input_file) + "_cleaned.md"
    result = full_text
    ### Regex Start
    result = re.sub(r'\*\s*','',result)
    result = re.sub(r'\.\n\s*\n•\n\s*','. ',result)
    # Figure
    result = re.sub(r'(Figure\s[0-9]{1,2})\.([0-9]{1,2})\n\n([A-Z].*)\n*\(.*\)*','## \g<1>-\g<2>\n\n\g<3> ![image_22-10-26_03_13_17](https://i.imgur.com/VNbeWv2.jpg)',result)
    result = re.sub(r'(Table\s[0-9]{1,2})\.([0-9]{1,2})\n\n([A-Z].*)\n*((\|(.*)\|\n)*)','## \g<1>-\g<2>\n\n\g<3>  ![image_22-10-26_03_13_17](https://i.imgur.com/VNbeWv2.jpg)',result)
    print("Do IT")
    result = re.sub(r'\</*[a-z]*\>','',result)
    result = re.sub(r'\(https\://www\.clinicalkey\S*\)','',result)
    result = re.sub(r'(## References)\n\n([0-9]{1,2}.*\n*\s*)*\[\[inbox]]','',result)
    result = re.sub(r'•\n\s*','',result)
    result = re.sub(r'\$','',result)

    with open(output_file, 'w+') as fp:
        fp.write(result)
    print(result)

if __name__ == '__main__':
    # split_all_paragraph(sys.argv[1],sys.argv[2])
    # clean_uptodate('uptodate.md')
    # clean_clinicalkey('ckey.md')
    md.fix_figure_table('outline.md')
    print("✨Done")

