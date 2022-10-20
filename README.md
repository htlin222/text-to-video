# text-to-video
[中文說明](ChineseREADME.md)
## Dependencis

- apply the azure text to speech service
- export the `SPEECH_KEY` and `SPEECH_REGION` to system env
	```
	export SPEECH_KEY='YOURSPEECH_KEY'
	export SPEECH_REGION='southeastasia'
	```
- or you can add them in `.zshrc` or `.bashrc`
- install the python package
	```shell
	pip install googletrans==4.0.0-rc1 azure-cognitiveservices-speech pypandoc
	```
- install the [FFmpeg](https://ffmpeg.org/)
	```
	brew install ffmpeg
	```

## Quick Start

- create a markdown file in the project directroy, and add the content in it
- then run the following command:
```shell
python main.py PROJECT.md
```
- the script will:
	- create a folder `PROJECT`
	- create : `translated.txt`, `outline.md`, `slide.pptx`, and `Audio.mp4` in the folder

## If you want to edit the translated text and export to audio files again:

- edit the `translated.txt` in your `PROJECT` folder
- after edit, in parent folder, run:
	```shell
	python text_to_speech.py PROJECT/translated.txt PROJECT
	```

## Open the `slide.pptx` by powerpoint, edit it, and export to images by:

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
