import pypandoc
import os
from pathlib import Path

def convert_to_pptx(filename, folder):
    output_file_path = folder + '/' + 'slide.pptx'
    output = pypandoc.convert_file(filename,
                                to='pptx',
                                outputfile=output_file_path,
                                extra_args=['--reference-doc=slidetemp.pptx'],
                                )

def create_output_folder(output_folder):
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, output_folder)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

if __name__ == '__main__':
    my_file = Path(sys.argv[1])
    create_output_folder(sys.argv[2])
    if my_file.is_file():
        convert_to_pptx(sys.argv[1], sys.argv[2])
        print("Done ~ ")
    else:
        print('please create file:', my_file, 'first, thank you.')
        file = open(sys.argv[1], 'w')
