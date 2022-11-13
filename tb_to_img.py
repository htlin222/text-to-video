# -*- coding: utf-8 -*-
import re
import sys
import os
import imgkit
from pathlib import Path
# https://pypi.org/project/imgkit/
# brew install --cask wkhtmltopdf
# https://dev.to/dcodeyt/creating-beautiful-html-tables-with-css-428l

options = {
    'format': 'png',
    'crop-h': '0',
    'crop-w': '3',
    'crop-x': '3',
    'crop-y': '3',
    'encoding': "UTF-8",
    'custom-header' : [ ('Accept-Encoding', 'gzip') ],
    'no-outline': None
}

# TODO: conver the table content to html
# https://www.digitalocean.com/community/tutorials/how-to-use-python-markdown-to-convert-markdown-text-to-html
def convert_to_image():
    with open('file.html') as f:
        imgkit.from_file('file.html', 'out.jpg',options=options, css=css)

# then upload to imgur

# imgkit.from_url('http://google.com', 'out.jpg')
# imgkit.from_file('test.html', 'out.jpg')
imgkit.from_string('Hello!', 'out.jpg')
