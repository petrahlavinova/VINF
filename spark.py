from pyspark.sql import SparkSession, functions, SQLContext
from pyspark.sql.types import StringType,MapType,StructType ,StructField    
from pyspark.sql import Row
from pyspark.sql.functions import col, when, coalesce,expr,broadcast
# import wikipedia
import requests
import re
import json
import os
import json
import sys
# wikipedia.set_lang("sk")
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

def get_wiki(book):
    try:
        page = wikipedia.page(book)
        return (page.url, page.title)
    except: 
        return None, None

def new_info(page_url):
    response = requests.get(page_url)
    if response.status_code == 200:
        html_content = response.text
        category_info_pattern = r'<div class=\"mw-content-ltr mw-parser-output\" lang=\"sk\" dir=\"ltr\">([\s\S]*?)(?=<\/p>)'
        category_info_match = re.search(category_info_pattern, html_content)
        category_info = category_info_match.group(1) if category_info_match else None
        if category_info_match:
            content_before_p = category_info_match.group(1)
            content_without_figure = re.sub(r'<figure\b[^>]*>.*?<\/figure>', '', content_before_p)
            category_info_clean = re.sub(r'<.*?>', '', content_without_figure)
            category_info_clean = re.sub(r'\[\d\]', '', category_info_clean)
            category_info_clean = re.sub(r'&#\d+', '', category_info_clean)
            category_info_clean = re.sub(r'\n', '', category_info_clean)
            category_info_clean = re.sub(r';\d+;', '', category_info_clean)
        # category_pattern = r'<span class="mw-page-title-main">(.*?)</span>'
        # category_match = re.search(category_pattern, html_content)
        # category = category_match.group(1) if category_match else None
        return category_info_clean
        


spark_session = SparkSession.builder.master('local[*]').appName('books_full').getOrCreate()
spark_session.conf.set("spark.sql.legacy.json.allowEmptyString.enabled", True)
schema = StructType([
      StructField("name",StringType(),False),
      StructField("original_name",StringType(),True),
      StructField("author",StringType(),True),
      StructField("category",StringType(),False),
      StructField("pages",StringType(),False),
      StructField("binding_type",StringType(),False),
      StructField("language",StringType(),False),
      StructField("publisher",StringType(),False),
      StructField("date_published",StringType(),False)
  ])

schema2 = StructType([
    StructField("category",StringType(),False),
    StructField("category_info",StringType(),False)
  ])

with open('books.json') as json_file:
    data = json.load(json_file)


with open('additional_book_info.json') as json_file:
    data2 = json.load(json_file)

info = spark_session.createDataFrame(data=data2,schema=schema2)
df = spark_session.createDataFrame(data=data,schema=schema)

result_df =  df.join(info, on="category")


json_string_rdd = result_df.toJSON()

import json

json_data = [json.loads(json_str) for json_str in json_string_rdd.collect()]
with open("pipik.json", "w",encoding='utf-8') as json_file:
    json.dump(json_data, json_file,ensure_ascii=False)

