from nltk.tree import Tree


class Flat:

    def __init__(self, parsed_sents, start='sentence'):
        self.start = start

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        t = Tree(self.start, [Tree(tag, [word]) for word, tag in tagged_sent])
        return t


class RBranch:

    def __init__(self, parsed_sents, start='sentence'):
        self.start = start

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        t = Tree(self.start, [Tree(tag, [word]) for word, tag in tagged_sent])
        t.chomsky_normal_form(factor='right', horzMarkov=0)
        return t
