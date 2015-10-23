# https://docs.python.org/3/library/unittest.html
from unittest import TestCase

from nltk.tree import Tree

from parsing.util import unlexicalize, spans


class TestSpans(TestCase):

    def test_spans(self):
        t = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                )
            """)

        s = spans(t)

        s2 = {('S', 0, 4), ('NP', 0, 1), ('VP', 2, 4), ('NP', 3, 4)}

        self.assertEqual(s, s2)

    def test_spans_doesnt_change_tree(self):
        t = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                )
            """)
        t2 = t.copy(deep=True)

        spans(t)

        self.assertEqual(t, t2)

    def test_spans_with_unary(self):
        t = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado)))
                )
            """)

        s = spans(t, unary=True)

        s2 = {('S', 0, 3), ('NP', 0, 1), ('VP', 2, 3), ('NP', 3, 3)}

        self.assertEqual(s, s2)


class TestUnlexicalize(TestCase):

    def test_unlexicalize(self):
        t = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                )
            """)

        ut = unlexicalize(t)

        ut2 = Tree.fromstring(
            """
                (S
                    (NP (Det Det) (Noun Noun))
                    (VP (Verb Verb) (NP (Noun Noun) (Adj Adj)))
                )
            """)

        self.assertEqual(ut, ut2)
