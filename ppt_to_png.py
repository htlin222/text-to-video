import os
import re
import sys
from pathlib import Path
import aspose.slides as slides
import aspose.pydrawing as drawing

# Load presentation
def pptx_to_png(folder):
    '''
    convert_to_png
    '''
    path_of_slide = folder + '/' + "slide.pptx"
    pres = slides.Presentation(path_of_slide)

    # Loop through slides
    for index in range(pres.slides.length):
        # Get reference of slide
        slide = pres.slides[index]

        # Save as PNG
        slide.get_thumbnail().save("slide_{i}.png".format(i = index), drawing.imaging.ImageFormat.png)

if __name__=='__main__':
    folder = Path(sys.argv[1])
    if os.path.exists(folder):
        pptx_to_png(folder)
        print("✨Have generated pptx and wav files in the [", folder, '] folder')
    else:
        print('❌ please create folder:', folder, 'first, thank you.')
        file = open(sys.argv[1], 'w')
