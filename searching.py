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

    def test_find_boolean_query1(self):
        name_parser = QueryParser("contents2", analyzer)
        name_query_obj = name_parser.parse('Ohnivé znamenie')
        category_parser = QueryParser("contents2", analyzer)
        category_query_obj = category_parser.parse('Beletria')
        boolean_query = BooleanQuery.Builder()
        boolean_query.add(name_query_obj, BooleanClause.Occur.MUST)
        boolean_query.add(category_query_obj, BooleanClause.Occur.MUST)
        scoreDoc = searcher.search(boolean_query.build(), 1).scoreDocs
        doc = searcher.doc(scoreDoc[0].doc)
        self.assertTrue('Ohnivé znamenie' in doc.get("name"))

    def test_find_one_query1(self):
        query = QueryParser("contents", analyzer).parse('Ohnivé znamenie')
        scoreDoc = searcher.search(query, 1).scoreDocs
        doc = searcher.doc(scoreDoc[0].doc)
        self.assertTrue('Ohnivé znamenie' in doc.get("name"))
    
    def test_find_boolean_query2(self):
        name_parser = QueryParser("contents2", analyzer)
        name_query_obj = name_parser.parse('Pečie celé Slovensko 2')
        category_parser = QueryParser("contents2", analyzer)
        category_query_obj = category_parser.parse('Kuchárske knihy')
        boolean_query = BooleanQuery.Builder()
        boolean_query.add(name_query_obj, BooleanClause.Occur.MUST)
        boolean_query.add(category_query_obj, BooleanClause.Occur.MUST)
        scoreDoc = searcher.search(boolean_query.build(), 1).scoreDocs
        doc = searcher.doc(scoreDoc[0].doc)
        self.assertTrue('Pečie celé Slovensko 2' in doc.get("name"))

    def test_find_one_query2(self):
        count = 0
        query = QueryParser("contents", analyzer).parse('Harry Potter')
        scoreDocs = searcher.search(query, 20).scoreDocs
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            if 'Harry Potter' in doc.get("name"):
                count += 1
        self.assertTrue(len(doc.get("name")) > 8)


    def test_not_find_boolean_query(self):
        name_parser = QueryParser("contents2", analyzer)
        name_query_obj = name_parser.parse('Bonifác')
        category_parser = QueryParser("contents2", analyzer)
        category_query_obj = category_parser.parse('Beletria')
        boolean_query = BooleanQuery.Builder()
        boolean_query.add(name_query_obj, BooleanClause.Occur.MUST)
        boolean_query.add(category_query_obj, BooleanClause.Occur.MUST)
        scoreDoc = searcher.search(boolean_query.build(), 1).scoreDocs
        self.assertEqual(len(scoreDoc), 0)

    def test_not_find_one_query(self):
        query = QueryParser("contents", analyzer).parse('Bonifác')
        scoreDoc = searcher.search(query, 1).scoreDocs
        self.assertEqual(len(scoreDoc), 0)

    def test_not_find_one_query2(self):
        query = QueryParser("contents", analyzer).parse('Ventilátor')
        scoreDoc = searcher.search(query, 1).scoreDocs
        self.assertEqual(len(scoreDoc), 0)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
directory = NIOFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()
while True:
    command = input("Choose one from \n1: One query\n2: Boolean query\n3: Unit tests\n4: Exit")
    if command == '1': runOneQuery(searcher, analyzer)
    elif command == '2': runBooleanQuery(searcher, analyzer)
    elif command == '3': unittest.main()
    elif command == '4': break
    else: print('Wrong input!')
del searcher