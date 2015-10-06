# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from tagging.features import History
from tagging.memm import MEMM


class TestMEMM(TestCase):

    def setUp(self):
        self.tagged_sents = [
            list(zip('el gato come pescado .'.split(),
                 'D N V N P'.split())),
            list(zip('la gata come salmón .'.split(),
                 'D N V N P'.split())),
        ]

    def test_sent_histories_1gram(self):
        model = MEMM(1, self.tagged_sents)

        hs = list(model.sent_histories(self.tagged_sents[0]))

        sent = 'el gato come pescado .'.split()
        hs2 = [
            History(sent, (), 0),
            History(sent, (), 1),
            History(sent, (), 2),
            History(sent, (), 3),
            History(sent, (), 4),
        ]
        self.assertEqual(hs, hs2)

    def test_sent_histories_2gram(self):
        model = MEMM(2, self.tagged_sents)

        hs = list(model.sent_histories(self.tagged_sents[0]))

        sent = 'el gato come pescado .'.split()
        hs2 = [
            History(sent, ('<s>',), 0),
            History(sent, ('D',), 1),
            History(sent, ('N',), 2),
            History(sent, ('V',), 3),
            History(sent, ('N',), 4),
        ]
        self.assertEqual(hs, hs2)

    def test_sent_histories_3gram(self):
        model = MEMM(3, self.tagged_sents)

        hs = list(model.sent_histories(self.tagged_sents[0]))

        sent = 'el gato come pescado .'.split()
        hs2 = [
            History(sent, ('<s>', '<s>'), 0),
            History(sent, ('<s>', 'D'), 1),
            History(sent, ('D', 'N'), 2),
            History(sent, ('N', 'V'), 3),
            History(sent, ('V', 'N'), 4),
        ]
        self.assertEqual(hs, hs2)

    def test_sents_histories_3gram(self):
        model = MEMM(3, self.tagged_sents)

        hs = list(model.sents_histories(self.tagged_sents))

        sent0 = 'el gato come pescado .'.split()
        sent1 = 'la gata come salmón .'.split()
        hs2 = [
            History(sent0, ('<s>', '<s>'), 0),
            History(sent0, ('<s>', 'D'), 1),
            History(sent0, ('D', 'N'), 2),
            History(sent0, ('N', 'V'), 3),
            History(sent0, ('V', 'N'), 4),
            History(sent1, ('<s>', '<s>'), 0),
            History(sent1, ('<s>', 'D'), 1),
            History(sent1, ('D', 'N'), 2),
            History(sent1, ('N', 'V'), 3),
            History(sent1, ('V', 'N'), 4),
        ]
        self.assertEqual(hs, hs2)

    def test_sent_tags(self):
        model = MEMM(3, self.tagged_sents)

        tags = list(model.sent_tags(self.tagged_sents[0]))
        self.assertEqual(tags, 'D N V N P'.split())

    def test_sents_tags(self):
        model = MEMM(3, self.tagged_sents)

        tags = list(model.sents_tags(self.tagged_sents))
        self.assertEqual(tags, 'D N V N P D N V N P'.split())

    def test_tag_history(self):
        models = [MEMM(i, self.tagged_sents) for i in [1, 2, 3]]

        result = 'D N V N P'.split()

        for model in models:
            hs = model.sent_histories(self.tagged_sents[0])
            for h, r in zip(hs, result):
                self.assertEqual(model.tag_history(h), r)

    def test_tag(self):
        models = [MEMM(i, self.tagged_sents) for i in [1, 2, 3]]

        sent = 'el gato come pescado .'.split()
        result = 'D N V N P'.split()

        for model in models:
            self.assertEqual(model.tag(sent), result)
