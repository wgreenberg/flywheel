from nltk.tokenize import sent_tokenize

def summarize(text: str) -> str:
    print(sent_tokenize(text))
    return 'The history of all hitherto existing society is the history of class struggles.'

if __name__ == '__main__':
    print(summarize('foo'))
