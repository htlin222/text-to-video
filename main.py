import generate_outline_markdown as md
import text_to_speech as tts
import translate_the_source as translate

def outline_translate_speech():
    md.open_file_then_set_outline('source.md','outline.md')
    translate.translate_to_zh('source.md','translated.txt')
    tts.text_to_speech('translated.txt')

if __name__=='__main__':
    outline_translate_speech()
