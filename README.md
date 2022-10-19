# text-to-video

## Dependencis

- apply the azure text to speech service
- export to `SPEECH_KEY` and `SPEECH_REGION` to system env
- install the python package
	```shell
	pip install googletrans==4.0.0-rc1 azure-cognitiveservices-speech pypandoc
	```
- install the ffmpeg
	```
	brew install ffmpeg
	```

## Quick Start

- create a markdown file in the project directroy, and add the content in it
- then run the following command:
```shell
python main.py PROJECT.md
```
- the script will do the following things:
	- create a folder name 'PROJECT'
	- it will create two files: `translated.txt`, and `outline.md` in that folder
	- create audio and pptx from them

## If you want to edit the translated text and export to audio files again:

- edit the `translated.txt` in your `PROJECT` folder
- run:
```shell
python text_to_speech.py PROJECT/translated.txt PROJECT
```

## Then open the `slide.pptx`, edit it, and export to images by:

- select the export type as png
- name the file as `slide`
- make sure the powerpoint have created the folder named `slide` in the `PROJECT` folder
- in the `slide` folder, you will see serial png files named `投影片1.png`...

## Finally, you can combine all the image and wav files into a mp4

- in command line, in the parent directroy, `../PROJECT`
- run:
	```
	python export_final.py PROJECT
	```
- you will get a file name `PROJECT_final.mp4` in `PROJECT` folder
