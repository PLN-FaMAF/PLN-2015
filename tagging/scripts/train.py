"""Train a sequence tagger.

Usage:
  train.py [-m <model>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger


models = {
    'base': BaselineTagger,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = corpus.tagged_sents()

    # train the model
    model = models[opts['-m']](sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
