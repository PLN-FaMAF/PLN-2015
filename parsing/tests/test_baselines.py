# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from nltk.tree import Tree

from parsing.baselines import Flat, RBranch, LBranch


class TestBaseline(TestCase):

    def setUp(self):
        self.tagged_sents = [
            list(zip('El gato come pescado .'.split(),
                 'D N V N P'.split())),
            list(zip('La gata come salmón .'.split(),
                 'D N V N P'.split())),
        ]

    def test_flat_parse(self):
        model = Flat([], 'S')  # empty training set

        trees = [model.parse(s) for s in self.tagged_sents]

        trees2 = [
            Tree.fromstring("(S (D El) (N gato) (V come) (N pescado) (P .))"),
            Tree.fromstring("(S (D La) (N gata) (V come) (N salmón) (P .))"),
        ]
        self.assertEqual(trees, trees2)

    def test_rbranch_parse(self):
        model = RBranch([], 'S')  # empty training set

        trees = [model.parse(s) for s in self.tagged_sents]

        trees2 = [
            Tree.fromstring("""(S (D El) (S|<> (N gato) (S|<> (V come) (S|<> (N pescado) (P .)))))"""),
            Tree.fromstring("""(S (D La) (S|<> (N gata) (S|<> (V come) (S|<> (N salmón) (P .)))))"""),
        ]
        self.assertEqual(trees, trees2)

    def test_lbranch_parse(self):
        model = LBranch([], 'S')  # empty training set

        trees = [model.parse(s) for s in self.tagged_sents]

        trees2 = [
            Tree.fromstring("""(S (S|<> (S|<> (S|<> (D El) (N gato)) (V come)) (N pescado)) (P .))"""),
            Tree.fromstring("""(S (S|<> (S|<> (S|<> (D La) (N gata)) (V come)) (N salmón)) (P .))"""),
        ]
        self.assertEqual(trees, trees2)
