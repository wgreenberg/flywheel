import asyncio

from math import log
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import EnglishStemmer

from graph import Vertex, Edge, Graph

stemmer = EnglishStemmer()

# like SxS, except we don't care about repeat values or order
def cartesian_square(S):
    for i, a in enumerate(S):
        for b in S[i+1:]:
            yield (a, b)

# from section 4.1
def similarity(a, b):
    shared_words = sentence_to_words(a) & sentence_to_words(b)
    return len(shared_words) / (log(len(a)) + log(len(b)))

def sentence_to_words(sentence):
    words = word_tokenize(sentence)
    stemmed = [stemmer.stem(w) for w in words]
    return set(stemmed)

def text_to_sentences(text):
    sentences = sent_tokenize(text)
    return filter(lambda s: len(s) > 1, sentences)

def summarize(text):
    print("Creating graph...")
    normalized_text = text.replace('”', '"')
    sentences = text_to_sentences(normalized_text)

    vertices = [Vertex(s) for s in sentences]

    edges = []
    for sent_a, sent_b in cartesian_square(vertices):
        score = similarity(sent_a.data, sent_b.data)
        edges.append(Edge(sent_a, sent_b, score))
        edges.append(Edge(sent_b, sent_a, score))

    g = Graph(vertices, edges)
    print("Graph initialized: %d nodes" % len(vertices))

    print("Running pagerank...")
    return g.sort_pagerank()

if __name__ == '__main__':
    import sys
    with open(sys.argv[1]) as f:
        sentences = summarize(f.read())
        for s in sentences[0:7]:
            print(s + '\n')
