INDEX_DIR = "IndexFilesFinal.index"

import sys
import os
import lucene
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BooleanClause, BooleanQuery
from org.apache.lucene.store import NIOFSDirectory
from org.apache.lucene.search import IndexSearcher
import tkinter as tk
from tkinter import Label, Entry, Button, Text, Scrollbar, END


def runBooleanQuery(searcher, analyzer, name_query, category_query, result_text):
    result_text.delete(1.0, END)  # Clear previous results

    print("Searching for: Name - {}, Category - {}".format(name_query, category_query))

    # Create two queries for name and category
    name_parser = QueryParser("contents2", analyzer)
    name_query_obj = name_parser.parse(name_query)

    category_parser = QueryParser("contents2", analyzer)
    category_query_obj = category_parser.parse(category_query)

    # Create a Boolean query with MUST clauses for name and category
    boolean_query = BooleanQuery.Builder()
    boolean_query.add(name_query_obj, BooleanClause.Occur.MUST)
    boolean_query.add(category_query_obj, BooleanClause.Occur.MUST)

    scoreDocs = searcher.search(boolean_query.build(), 50).scoreDocs
    result_text.insert(tk.END, "{} total matching documents.\n".format(len(scoreDocs)))

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        result_text.insert(tk.END, 'name: {}\n'.format(doc.get("name")))
        result_text.insert(tk.END, 'author: {}\n'.format(doc.get("author")))
        result_text.insert(tk.END, 'category: {}\n\n'.format(doc.get("category")))


def on_search_button_click(entry_name, entry_category, result_text, searcher, analyzer):
    name_query = entry_name.get()
    category_query = entry_category.get()
    runBooleanQuery(searcher, analyzer, name_query, category_query, result_text)


def create_gui(searcher, analyzer):
    root = tk.Tk()
    root.title("Lucene Search GUI")

    label_name = Label(root, text="Name:")
    label_name.grid(row=0, column=0, sticky="E")

    entry_name = Entry(root)
    entry_name.grid(row=0, column=1)

    label_category = Label(root, text="Category:")
    label_category.grid(row=1, column=0, sticky="E")

    entry_category = Entry(root)
    entry_category.grid(row=1, column=1)

    search_button = Button(root, text="Search", command=lambda: on_search_button_click(entry_name, entry_category, result_text, searcher, analyzer))
    search_button.grid(row=2, column=0, columnspan=2)

    result_text = Text(root, wrap=tk.WORD, height=10, width=50)
    result_text.grid(row=3, column=0, columnspan=2)

    scrollbar = Scrollbar(root, command=result_text.yview)
    scrollbar.grid(row=3, column=2, sticky="NS")
    result_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()


lucene.initVM(vmargs=['-Djava.awt.headless=true'])
print('lucene', lucene.VERSION)
base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
directory = NIOFSDirectory(Paths.get(os.path.join(base_dir, INDEX_DIR)))
searcher = IndexSearcher(DirectoryReader.open(directory))
analyzer = StandardAnalyzer()
create_gui(searcher, analyzer)
del searcher
