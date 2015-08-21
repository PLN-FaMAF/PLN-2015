# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from math import log

from languagemodeling.ngram import InterpolatedNGram


class TestInterpolatedNGram(TestCase):

    def setUp(self):
        self.sents = [
            'el gato come pescado .'.split(),
            'la gata come salmón .'.split(),
        ]

    def test_init_1gram(self):
        model = InterpolatedNGram(1, self.sents, gamma=1.0)

        counts = {
            (): 12,
            ('el',): 1,
            ('gato',): 1,
            ('come',): 2,
            ('pescado',): 1,
            ('.',): 2,
            ('</s>',): 2,
            ('la',): 1,
            ('gata',): 1,
            ('salmón',): 1,
        }
        for gram, c in counts.items():
            self.assertEqual(model.count(gram), c)

    def test_cond_prob_1gram_no_addone(self):
        model = InterpolatedNGram(1, self.sents, gamma=1.0, addone=False)

        # behaves just like unsmoothed n-gram
        probs = {
            'pescado': 1 / 12.0,
            'come': 2 / 12.0,
            'salame': 0.0,
        }
        for token, p in probs.items():
            self.assertEqual(model.cond_prob(token), p)

    def test_cond_prob_2gram_no_addone(self):
        gamma = 1.0
        model = InterpolatedNGram(2, self.sents, gamma, addone=False)

        c1 = 2.0  # count for 'come'
        l1 = c1 / (c1 + gamma)

        probs = {
            ('pescado', 'come'): l1 * 0.5 + (1.0 - l1) * 1 / 12.0,
            ('salmón', 'come'): l1 * 0.5 + (1.0 - l1) * 1 / 12.0,
            ('salame', 'come'): 0.0,
        }
        for (token, prev), p in probs.items():
            self.assertEqual(model.cond_prob(token, [prev]), p, (token))
