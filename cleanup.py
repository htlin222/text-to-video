#!/usr/bin/env python3
import re
import sys
import os
from pathlib import Path
import generate_outline_markdown as md

input_file = 'break.md'
output_file = 'done_break.md'

def split_single_paragraph(paragraph):
    import re
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

def clear_uptodate(input_file):
    with open(input_file, 'r') as file:
        full_text = file.read()
    # Remove the context below the title
    result = re.sub(r'(#\s(.*)- UpToDate)\n((.*\n)*)(INTRODUCTION)',"",full_text)
    result = re.sub(r'',"",result)


    print("🥟 Uptodate is clear")

if __name__ == '__main__':
    split_all_paragraph(sys.argv[1],sys.argv[2])
    print("✨Done")

