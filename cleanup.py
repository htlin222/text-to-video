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

def clean_uptodate(input_text):
    '''
    search pattern in uptodate and clean up
    '''
    print("Start cleanup ⬆️  UpToDate style")
    # Remove the context below the title
    result = input_text
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
    result = re.sub(r'\(https://www.uptodate.com/[^\)]*\)','',result)

    result = re.sub(r'(\\\[|\\\])','',result)
    result = re.sub(r'(\[[0-9]{1,2}((-|,)[0-9]{1,2})*\])','',result)
    result = re.sub(r'\[("|\')(.*)("|\')\]','"\g<2>"',result)
    result = re.sub(r'<(/*)sup>','',result)
    result = re.sub(r'\[([A-Za-z][a-z]*)\]','\g<1>',result)
    result = re.sub(r'(●)(.*\n)\n', '\g<2>',result)
    result = re.sub(r'\[inbox\]','',result)
    result = re.sub(r'\*\*','',result)
    return result


def clean_clinicalkey(input_text):
    '''
    according to clincalkey markdown
    '''
    print("Start cleanup ⬆️  ClinicalKey style")
    result = input_text
    ### Regex Start
    result = re.sub(r'(\n\n\*\s*)(•|[0-9]\))\n.*\n\s*([A-Za-z])','. \g<2> \g<3>',result)
    result = re.sub(r'\*\s*([0-9])\.\n\n\s*([A-Za-z])','Point: \g<1>. \g<2>',result)
    result = re.sub(r'\.\n\s*\n•\n\s*','. ',result)
    result = re.sub(r'([0-9]{1,2})\n\n((#{1,2}))','\g<1>',result)
    result = figure_table(result)
    result = re.sub(r'\</*[a-z]*\>','',result)
    result = re.sub(r'\(https\://www\.clinicalkey\S*\)','',result)
    result = re.sub(r'(## (References))\n\n([0-9]{1,2}.*\n*\s*)*\[\[inbox]]','',result)
    result = re.sub(r'## Suggested.*\n*(.*\n*)*','',result)
    result = re.sub(r'•\n\s*','',result)
    result = re.sub(r'\$','',result)
    return result

# TODO: NEJM
def clean_nejm(full_text):
    result = full_text
    ### Regex Here~
    return result
def clean_harison(full_text):
    result = full_text
    result = figure_table(result)
    return result

def figure_table(text):
    result_fig_tab = text
    # Figure
    result_fig_tab = re.sub(r'((Figure|FIGURE|FIG|Fig)\.*\s[0-9]{1,2})\.([0-9]{1,2})\n\n([A-Z].*)\n*\(.*\)*','\g<3> ![\g<1>-\g<2>](https://i.imgur.com/VNbeWv2.jpg)',result_fig_tab)
    # Table
    result_fig_tab = re.sub(r'((Table|TABLE)\.*\s[0-9]{1,2})\.([0-9]{1,2})\n\n([A-Z].*)\n*((\|(.*)\|\n)*)','\g<3> ![\g<1>-\g<2>](https://i.imgur.com/VNbeWv2.jpg)',result_fig_tab)
    return result_fig_tab

def clean_all(input_file,output_file):
    with open(input_file, 'r') as file:
        full_text = file.read()
    result = full_text
    # result = clean_uptodate(result)
    result = clean_nejm(result)
    result = clean_clinicalkey(result)
    result = figure_table(result)
    with open(output_file, 'w+') as fp:
        fp.write(result)

if __name__ == '__main__':
    newfile = "cleaned_" + sys.argv[1]
    output_file = os.path.join(sys.argv[2],newfile)
    clean_all(sys.argv[1],output_file)
    # md.fix_figure_table('outline.md')
    print("🚿 Cleaned, file is at", output_file)

