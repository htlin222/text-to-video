# text-to-video

## Dependencis

- python package
- pandoc


## How to use

### Text to speech 

- add content to `original.txt`
- run `translate-the-original.py`
- the result will be in `translated.txt`
- run `text-to-speech.py`
- the result will be in `output/file.wav`

### Generate the slide

- run `generate-markdown.py`
- result will be in `md-to-slide.md`
- run `pandoc`
- the result will be in `slide-result.pptx`
