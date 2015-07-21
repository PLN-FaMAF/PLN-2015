# https://docs.python.org/3/library/collections.html
from collections import defaultdict


class NGram(object):
    
    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """

        self.counts = counts = defaultdict(int)

        for sent in sents:
            for i in range(len(sent) - n + 1):
                if n == 1:
                    ngram = sent[i]
                else:
                    ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
