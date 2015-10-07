from nltk.corpus.reader.api import SyntaxCorpusReader
from nltk.corpus.reader import xmldocs
from nltk import tree
from nltk.util import LazyMap, LazyConcatenation
from nltk.corpus.reader.util import concat


def parsed(element):
    """Converts a 'sentence' XML element (xml.etree.ElementTree.Element) to
    an NLTK tree.

    element -- the XML sentence element (or a subelement)
    """
    if element:
        # element viewed as a list is non-empty (it has subelements)
        subtrees = map(parsed, element)
        subtrees = [t for t in subtrees if t is not None]
        return tree.Tree(element.tag, subtrees)
    else:
        # element viewed as a list is empty. we are in a terminal.
        if element.get('elliptic') == 'yes':
            return None
        else:
            return tree.Tree(element.get('pos') or element.get('ne') or 'unk',
                             [element.get('wd')])


def tagged(element):
    """Converts a 'sentence' XML element (xml.etree.ElementTree.Element) to
    a tagged sentence.

    element -- the XML sentence element (or a subelement)
    """
    # http://www.w3schools.com/xpath/xpath_syntax.asp
    # XXX: XPath '//*[@wd]' not working
    # return [(x.get('wd'), x.get('pos') or x.get('ne'))
    #         for x in element.findall('*//*[@wd]')] + [('.', 'fp')]

    # convert to tree and get the tagged sent
    pos = parsed(element).pos()
    # filter None words (may return an emtpy list)
    return list(filter(lambda x: x[0] is not None, pos))


def untagged(element):
    """Converts a 'sentence' XML element (xml.etree.ElementTree.Element) to
    a sentence.

    element -- the XML sentence element (or a subelement)
    """
    # http://www.w3schools.com/xpath/xpath_syntax.asp
    # XXX: XPath '//*[@wd]' not working
    # return [x.get('wd') for x in element.findall('*//*[@wd]')] + [('.', 'fp')]

    # convert to tree and get the sent
    sent = parsed(element).leaves()
    # filter None words (may return an emtpy list)
    return list(filter(lambda x: x is not None, sent))


class AncoraCorpusReader(SyntaxCorpusReader):

    def __init__(self, path, files=None):
        if files is None:
            files = '.*\.tbf\.xml'
        self.xmlreader = xmldocs.XMLCorpusReader(path, files)

    def parsed_sents(self, fileids=None):
        return LazyMap(parsed, self.elements(fileids))

    def tagged_sents(self, fileids=None):
        return LazyMap(tagged, self.elements(fileids))

    def sents(self, fileids=None):
        return LazyMap(untagged, self.elements(fileids))

    def elements(self, fileids=None):
        # FIXME: skip sentence elements that will result in empty sentences!
        if not fileids:
            fileids = self.xmlreader.fileids()
        # xml() returns a top element that is also a list of sentence elements
        return LazyConcatenation(self.xmlreader.xml(f) for f in fileids)

    def tagged_words(self, fileids=None):
        return LazyConcatenation(self.tagged_sents(fileids))

    def __repr__(self):
        return '<AncoraCorpusReader>'


class SimpleAncoraCorpusReader(AncoraCorpusReader):
    """Ancora corpus with simplified POS tagset.
    """

    def __init__(self, path, files=None):
        super().__init__(path, files)

    def tagged_sents(self, fileids=None):
        f = lambda s: [(w, t[:2]) for w, t in s]
        return LazyMap(f, super().tagged_sents(fileids))
