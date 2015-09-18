from nltk.corpus.reader.api import SyntaxCorpusReader
from nltk.corpus.reader import xmldocs
from nltk import tree
from nltk.util import LazyMap
from nltk.corpus.reader.util import concat


def parsed(element):
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
            return tree.Tree(element.get('pos') or element.get('ne') or 'unk', [element.get('wd')])


def tagged(element):
    # http://www.w3schools.com/xpath/xpath_syntax.asp
    # XXX: XPath '//*[@wd]' not working
    #return [(x.get('wd'), x.get('pos') or x.get('ne')) for x in element.findall('*//*[@wd]')] + [('.', 'fp')]
    return list(filter(lambda x: x != (None, None), parsed(element).pos()))


def untagged(element):
    # http://www.w3schools.com/xpath/xpath_syntax.asp
    # XXX: XPath '//*[@wd]' not working
    #return [x.get('wd') for x in element.findall('*//*[@wd]')] + [('.', 'fp')]
    return list(filter(lambda x: x is not None, parsed(element).leaves()))


class AncoraCorpusReader(SyntaxCorpusReader):

    def __init__(self, path, files=None):
        if files is None:
            files = '.*\.tbf\.xml'
        self.xmlreader = xmldocs.XMLCorpusReader(path, files)
    
    def parsed_sents(self, fileids=None):
        if not fileids:
            fileids = self.xmlreader.fileids()
        return LazyMap(parsed, concat([list(self.xmlreader.xml(fileid)) for fileid in fileids]))

    def tagged_sents(self, fileids=None):
        if not fileids:
            fileids = self.xmlreader.fileids()
        return LazyMap(tagged, concat([list(self.xmlreader.xml(fileid)) for fileid in fileids]))

    def sents(self, fileids=None):
        # FIXME: not lazy!
        if not fileids:
            fileids = self.xmlreader.fileids()
        return LazyMap(untagged, concat([list(self.xmlreader.xml(fileid)) for fileid in fileids]))

    def tagged_words(self, fileids=None):
        return concat(self.tagged_sents(fileids))

    def __repr__(self):
        return '<AncoraCorpusReader>'


class SimpleAncoraCorpusReader(AncoraCorpusReader):
    """Ancora corpus with simplified POS tagset.
    """

    def __init__(self, path, files=None):
        super().__init__(path, files)

    def tagged_sents(self, fileids=None):
        return LazyMap(lambda s: [(w, t[:2]) for w, t in s], super().tagged_sents(fileids))
