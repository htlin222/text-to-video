import pypandoc
import os

def convert_to_pptx(filename, folder):
    output_file_path = folder + '/' + 'slide.pptx'
    output = pypandoc.convert_file(filename,
                                to='pptx',
                                outputfile=output_file_path,
                                extra_args=['--reference-doc=slidetemp.pptx'],
                                )

if __name__ == '__main__':
    convert_to_pptx('test.md','lizard')
