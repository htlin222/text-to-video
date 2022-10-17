import re
import os

def read_file(filename):
    textfile = open(filename, 'r')
    filetext = textfile.read()
    return filetext
if __name__=='__main__':
    filetext = read_file('test.md')
    print(filetext)
