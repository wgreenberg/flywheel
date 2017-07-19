import sys

from lib.summarizer import summarize

with open(sys.argv[1]) as f:
    sentences = summarize(f.read())
    for s in sentences[0:7]:
        print(s + '\n')
