

def unlexicalize(t):
    """Unlexicalize a tree. Overwrites the terminals with the pre-terminals.

    t -- the tree.
    """
    for p in t.treepositions('leaves'):
        tag = t[p[:-1]].label()
        t[p] = tag

    return t


def lexicalize(t, sent):
    """Lexicalize a tree using a sentence. Replaces the terminals with the words
    in the sentence.

    t -- the tree.
    sent -- the sentence.
    """
    for w, p in zip(sent, t.treepositions('leaves')):
        t[p] = w

    return t


def spans(t, unary=False):
    """Return the list of spans of a tree, each span being a triple (n, i, j),
    where n is the non-terminal and (i, j) is the sentence interval.

    t -- the tree.
    unary -- whether to return the unary productions (default: False).
    """
    t2 = t.copy(deep=True)
    for i, p in enumerate(t2.treepositions('leaves')):
        t2[p] = i
    result = set()

    def f(t):
        return (unary or len(t) > 1) and t.height() > 2

    for st in t2.subtrees(filter=f):
        leaves = st.leaves()
        span = (st.label(), leaves[0], leaves[-1])
        result.add(span)

    return result
