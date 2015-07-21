# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from languagemodeling.ngram import NGram


class TestNGram(TestCase):

    def test_init_1gram(self):

        sents = [
            'el gato come pescado .'.split(),
            'la gata come salmón .'.split(),
        ]

        ngram = NGram(1, sents)

        counts = {
            'el': 1,
            'gato': 1,
            'come': 2,
            'pescado': 1,
            '.': 2,
            'la': 1,
            'gata': 1,
            'salmón': 1,
        }

        self.assertEqual(dict(ngram.counts), counts)

    def test_init_2gram(self):

        sents = [
            'el gato come pescado .'.split(),
            'la gata come salmón .'.split(),
        ]

        ngram = NGram(2, sents)

        counts = {
            ('el', 'gato'): 1,
            ('gato', 'come'): 1,
            ('come', 'pescado'): 1,
            ('pescado', '.'): 1,
            ('la', 'gata'): 1,
            ('gata', 'come'): 1,
            ('come', 'salmón'): 1,
            ('salmón', '.'): 1,
        }

        self.assertEqual(dict(ngram.counts), counts)
