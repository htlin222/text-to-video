import re
text = 'My number is 415-555-4242.'
text = '##My number is 415-555-4242.##'
def find_title(text):
    titleRegex = re.compile(r'##\s*([A-Za-z].*)\s*##')
    title = re.findall(titleRegex, str(text))
    if not title == []
    :
        return title[0]
    else:
        return '重點: '

print(find_title(text))
