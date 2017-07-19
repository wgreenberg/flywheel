from functools import lru_cache
from itertools import combinations
from math import log
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem.snowball import EnglishStemmer

from lib.graph import Vertex, Edge, Graph

stemmer = EnglishStemmer()

# from section 4.1
def similarity(sentence_a, sentence_b):
    words_a = sentence_to_words(sentence_a)
    words_b = sentence_to_words(sentence_b)
    return len(words_a & words_b) / (log(len(words_a)) + log(len(words_b)))

@lru_cache(maxsize=1024)
def sentence_to_words(sentence):
    words = word_tokenize(sentence)
    stemmed = [stemmer.stem(w) for w in words]
    return set(stemmed)

def text_to_sentences(text):
    normalized_text = text.replace('”', '"')
    sentences = sent_tokenize(normalized_text)
    return filter(lambda s: len(s) > 1, sentences)

def summarize(text):
    print("Creating graph...")
    vertices = [Vertex(s) for s in text_to_sentences(text)]
    edges = []

    for sentence_a, sentence_b in combinations(vertices, 2):
        score = similarity(sentence_a.data, sentence_b.data)
        edges.append(Edge(sentence_a, sentence_b, score))
        edges.append(Edge(sentence_b, sentence_a, score))

    # drop the memoized entries
    sentence_to_words.cache_clear()

    g = Graph(vertices, edges)
    print("Graph initialized: |V|=%d, |E|=%d" % (len(vertices), len(edges)))

    print("Running pagerank...")
    return g.sort_pagerank()
