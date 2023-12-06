INDEX_DIR = "IndexFilesFinal.index"

import sys, os, lucene
import unittest
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BooleanClause, BooleanQuery
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher

def runOneQuery(searcher, analyzer):
    while True:
        print
        command = input("Name:")
        if command == '':
            return

        print
        print("Searching for:", command)
        query = QueryParser("contents", analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print('Book name:', doc.get("name"), ", Author: ", doc.get("author"))
def runBooleanQuery(searcher, analyzer):
    while True:
        print()
        name_query = input("Name:")
        category_query = input("Category:")

        if name_query == '' and category_query == '':
            return

        print("Searching for: Name - {}, Category - {}".format(name_query, category_query))

        # Vytvorenie dvoch dotazov pre meno a kategóriu
        name_parser = QueryParser("contents2", analyzer)
        name_query_obj = name_parser.parse(name_query)

        category_parser = QueryParser("contents2", analyzer)
        category_query_obj = category_parser.parse(category_query)

        # Vytvorenie logického dotazu OR pre meno a kategóriu
        boolean_query = BooleanQuery.Builder()
        boolean_query.add(name_query_obj, BooleanClause.Occur.MUST)
        boolean_query.add(category_query_obj, BooleanClause.Occur.MUST)

        scoreDocs = searcher.search(boolean_query.build(), 50).scoreDocs
        print("%s total matching documents." % len(scoreDocs))

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print('name:', doc.get("name"))
            print('author:', doc.get("author"))
            print('category:', doc.get("category"))
            print('category info:', doc.get("category_info"))
            print('______________________')


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
directory = NIOFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()
runBooleanQuery(searcher, analyzer)
unittest.main()
del searcher