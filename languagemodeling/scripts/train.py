"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import gutenberg

from languagemodeling.ngram import NGram


if __name__ == '__main__':
    opts = docopt(__doc__)
    print(opts)

    # load the data
    sents = gutenberg.sents('austen-emma.txt')

    # train the model
    n = opts['-n']
    model = NGrams(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'w')
    pickle.dump(model, f)
    f.close()
