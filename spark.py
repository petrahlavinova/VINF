from pyspark.sql import SparkSession, functions, SQLContext
from pyspark.sql.types import StringType
from pyspark.sql import Row
import wikipedia
import requests
import re
import json

wikipedia.set_lang("sk")

def get_wiki(book):
    try:
        page = wikipedia.page(book)
        return (page.url)
    except: 
        return None

def new_info(page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        html_content = response.text
        born_pattern = r'<div class=\"mw-content-ltr mw-parser-output\" lang=\"sk\" dir=\"ltr\"><p>(.*?)\s*<\/p>'
        born_match = re.search(born_pattern, html_content)
        born = born_match.group(1) if born_match else None
        born_clean = re.sub(r'<.*?>', '', born)
        return born_clean
        

with open('books1.json', 'r', encoding='utf-8') as file:
    books = json.load(file)
    new_data = []
    for book in books:
        book_category = book['category']
        print(book_category)
        book_category_page = get_wiki(book_category)
        if book_category_page:
            clean_new_info = new_info(book_category_page)
            print(clean_new_info)
#             book["category_info"] = clean_new_info

# # Uloženie do JSON
# with open('books1.json', 'w', encoding='utf-8') as file:
#     json.dump(books, file, ensure_ascii=False, indent=2)


            new_book = {
                "book_name": book["name"],
                "category_info": clean_new_info
            }
            new_data.append(new_book)

# Uloženie nových údajov do nového JSON súboru
with open('additional_book_info.json', 'w', encoding='utf-8') as file:
    json.dump(new_data, file, ensure_ascii=False, indent=2)

#spark_session = SparkSession.builder.master('local[*]').appName('books_full').getOrCreate()
#df = spark_session.read.text('books.json')