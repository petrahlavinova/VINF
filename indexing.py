INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, time
from datetime import datetime

from java.nio.file import Paths
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import \
    FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.store import NIOFSDirectory


class Ticker(object):

    def __init__(self):
        self.tick = True

def IndexFiles(root, storeDir, analyzer):

    if not os.path.exists(storeDir):
        os.mkdir(storeDir)

    store = NIOFSDirectory(Paths.get(storeDir))
    analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    print('Start of Indexing...')
    indexDocs(root, writer)
    print('Commit index...',)
    writer.commit()
    writer.close()
    print('Done')

def indexDocs(root, writer):

    t1 = FieldType()
    t1.setStored(True)
    t1.setTokenized(False)
    t1.setIndexOptions(IndexOptions.DOCS_AND_FREQS)

    t2 = FieldType()
    t2.setStored(False)
    t2.setTokenized(True)
    t2.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if not filename.endswith('.txt'):
                continue
            print("adding", filename)

            path = os.path.join(root, filename)
            file = open(path, "r", encoding="utf-8")
            contents = file.read()
            file.close()
            doc = Document()
            doc.add(Field("name", filename, t1))
            doc.add(Field("path", root, t1))
            if len(contents) > 0:
                doc.add(Field("contents", contents, t2))
            else:
                print("warning: no content in %s" % filename)
            writer.addDocument(doc)


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)
start = datetime.now()
root_folder = "books_txt_files/"
base_dir = os.path.dirname(os.path.abspath(root_folder))
IndexFiles(base_dir, os.path.join(base_dir, INDEX_DIR),
                StandardAnalyzer())
end = datetime.now()
print(end - start)