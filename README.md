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

## TODO:

- export serial image to audio
```shell
ffmpeg -i image1.png -i image2.png -i audio1.wav -i audio2.wav
  -filter_complex
     "[0]setsar=1[a];
      [1]pad=W:H:(ow-iw)/2:(oh-ih)/2:color=white,setsar=1[b];
      [2]abitscope=r=25:s=WxH[a1v]; 
      [3]abitscope=r=25:s=WxH[a2v];
      [a1v][a]overlay[v1];
      [a2v][b]overlay[v2];
      [v1][2:a][v2][3:a]concat=n=2:v=1:a=1"  out.mp4  
```
- or try this
```shell
ffmpeg -i slide_1.png -i speech_1.wav clip_1.mp4
ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.mp4
```
