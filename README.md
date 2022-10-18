# text-to-video

## Dependencis

- apply the azure text to speech service
- export to `SPEECH_KEY` and `SPEECH_REGION` to system env
- install the python package
```shell
pip install googletrans==4.0.0-rc1 azure-cognitiveservices-speech pypandoc
```

## Quick Start

- edit `source.md` in the current directroy, and add the content in it
- then run the following command:
```shell
python main.py source.md output_folder
```
- it will create two files: `translated.txt`, and `outline.md` in current directroy
- then create audio and pptx from them
- the audio and pptx will be in `output_folder`

## if you want to edit the translated text and export again:

- edit the `translated.txt`
- run:
```shell
python text_to_speech.py translated.txt output_folder
```
