import os
import json
import re
import time


books = []
directory = "books_txt_files"

start = time.time()


for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
                    
            title_pattern = r'<h1 class="mb-1" itemprop="name">\s+(.*?)\s+</h1>'
            title_match = re.search(title_pattern, html_content)
            book_title = title_match.group(1) if title_match else None

            author_pattern2 = r'<h2 class=\"pb-2 pb-sm-3 mb-2 mb-sm-3\">\n\s+(.*?)\s+<\/h2>'
            author_pattern3 = r'class=\"author\"\s>(.*?),*<\/a>'
            author_pattern1 = r'<h2 class=\"pb-2 pb-sm-3 mb-2 mb-sm-3\">\n\s+<div class=\"author\"\s>(.*?)<\/div>\s+<\/h2>'
            author_match2 = re.search(author_pattern2, html_content)
            author_match1 = re.search(author_pattern1, html_content)
            if author_match1:
                author_name = author_match1.group(1)
            elif author_match2:
                author_name = author_match2.group(1)
                author_match3 = re.findall(author_pattern3, html_content)
                author_name = ', '.join(author_match3)
            else:
                author_name = None

            
            category_pattern = r'<span itemprop="name">\s+(.*?)\s+</span>\s+</a>\s+<meta itemprop="position" content="3">'
            category_match = re.search(category_pattern, html_content)
            category = category_match.group(1) if category_match else None

            pages_pattern = r'<strong class="col-auto">Počet strán:</strong>\s+(\d+)\s+</li>'
            pages_match = re.search(pages_pattern, html_content)
            number_of_pages = pages_match.group(1) if pages_match else None

            binding_pattern = r'<strong class="col-auto">Väzba:</strong>\s+(.*?)\s+</li>'
            binding_match = re.search(binding_pattern, html_content)
            binding_type = binding_match.group(1) if binding_match else None

            original_name_pattern = r'<strong class="col-auto">Pôvodný názov:</strong>\s+(.*?)\s+</li>'
            original_name_match = re.search(original_name_pattern, html_content)
            original_name = original_name_match.group(1) if original_name_match else None

            ean_pattern = r'<strong class="col-auto">EAN:</strong>\s+(\d+)\s+</li>'
            ean_match = re.search(ean_pattern, html_content)
            ean = ean_match.group(1) if ean_match else None

            language_pattern = r'<strong class="col-auto">Jazyk:</strong>\s+([\w]+)\s+</li>'
            language_match = re.search(language_pattern, html_content)
            language = language_match.group(1) if language_match else None

            date_pattern = r'<strong class="col-auto">Dátum vydania:</strong>\s+(\d+\.\s+\w+\s+\d{4})\s+</li>'
            date_match = re.search(date_pattern, html_content)
            publication_date = date_match.group(1) if date_match else None

            publisher_pattern = r'class="text-dark text-underline">\n\s+(.*?)\s+<\/a>'
            publisher_match = re.search(publisher_pattern, html_content)
            publisher_name = publisher_match.group(1) if publisher_match else None

        
        if book_title and author_name and number_of_pages and binding_type and language and publication_date and publisher_name:
            book_info = {
                "name": book_title,
                "original_name": original_name,
                "author": author_name,
                "category": category,
                "pages": number_of_pages,
                "binding_type": binding_type,
                "language": language,
                "publisher": publisher_name,
                "date_published": publication_date
            }
            
            print(book_info)
            books.append(book_info)


output_file = "book_information.json"
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(books, json_file, ensure_ascii=False, indent=4)

print(f"Extracted information from {len(books)} books and saved to {output_file}")


end = time.time()
print("Time elapsed: ",end - start)
 