import sys, os, lucene, time
from datetime import datetime
import json

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import NIOFSDirectory

INDEX_DIR = "IndexFilesFinal.index"

class Ticker(object):
    def __init__(self):
        self.tick = True

def IndexFiles(books_json_path, storeDir, analyzer):
    if not os.path.exists(storeDir):
        os.mkdir(storeDir)

    # create a Lucene NIOFSDirectory for storing the index
    store = NIOFSDirectory(Paths.get(storeDir))
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
     # configuration for IndexWriter
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
     # create an IndexWriter
    writer = IndexWriter(store, config)

    print('Start of Indexing...')
    indexDocs(books_json_path, writer)
    writer.commit()
    writer.close()

def indexDocs(books_json_path, writer):
     # define field types
    t1 = FieldType()
    t1.setStored(True)
    t1.setTokenized(False)
    t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    t2 = FieldType()
    t2.setStored(False)
    t2.setTokenized(True)
    t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    with open(books_json_path, 'r', encoding='utf-8') as json_file:
        books = json.load(json_file)

         # creating Lucene document for indexing for each book
        for book in books:
            # relevant information of book
            name = book.get("name", "")
            author = book.get("author", "")
            category = book.get("category", "")
            category = book.get("category_info", "")
            contents = f"{name} {author}"
            contents2 = f"{name} {category}"

            # creating a Lucene document
            doc = Document()
            doc.add(Field("name", name, t1))
            doc.add(Field("author", author, t1))
            doc.add(Field("category", category, t1))
            doc.add(Field("category_info", category, t1))
            doc.add(Field("contents", contents, t2))
            doc.add(Field("contents2", contents2, t2))
            writer.addDocument(doc)

lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)
start = datetime.now()
books_json_path = "books_complete.json"
IndexFiles(books_json_path, INDEX_DIR, StandardAnalyzer())
end = datetime.now()
print(end - start)
