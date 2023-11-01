import os
import requests
import re
import time

# Function to download a page and save it as a .txt file
def save_page_as_txt(url, file_name):
    response = requests.get(url)
    
    if response.status_code == 200:
        # Save the content to a .txt file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        print(f"Saved page: {url} as {file_name}")
    else:
        print(f"Failed to retrieve page: {url}")

# Function to extract links with a specific pattern from a page
def extract_links_with_pattern(url):
    response = requests.get(url)
    links = re.findall(f'href=["\'](https://bookshop.org/p/books/.*?)(?=["\'])', response.text)
    return links

start = time.time()

# Create a directory to store the .txt files
output_directory = "bookshop_txt_pages"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Starting URL
start_url = "https://bookshop.org/categories/m"
pages_to_crawl = [start_url]

# Set a limit to the number of pages to crawl to avoid infinite loops
crawl_limit = 50

pagination_pattern = r'<span class="last"><a href="([^"]+)">(\d+)</a></span>'
pagination_count = re.search(pagination_pattern, start_url)
print(pagination_count)
if pagination_count:
    last_page_number = pagination_count.group(2)
    print("Last Page Number:", last_page_number)
# A set to keep track of visited URLs
visited_urls = set()

# Iterate through the pages and save each as a .txt file
while pages_to_crawl and crawl_limit > 0:
    current_url = pages_to_crawl.pop(0)
    
    # Check if the URL has already been visited
    if current_url in visited_urls:
        continue
    
    visited_urls.add(current_url)
    
    # Generate a valid file name based on the URL
    file_name = os.path.join(output_directory, f"page_{len(visited_urls)}.txt")
    save_page_as_txt(current_url, file_name)
    
    # Extract links to book pages from the current page
    book_links = extract_links_with_pattern(current_url)
    
    # Save the book page links
    for book_link in book_links:
        book_file_name = os.path.join(output_directory, f"book_{len(visited_urls)}_page.txt")
        save_page_as_txt(book_link, book_file_name)
    
    # Extract links to next category pages and add them to the pages to crawl
    response = requests.get(current_url)
    if response.status_code == 200:
        next_category_links = re.findall(r'href=["\'](https://bookshop.org/categories/m\?page=\d+)(?=["\'])', response.text)
        for next_category_link in next_category_links:
            if next_category_link not in pages_to_crawl:
                pages_to_crawl.append(next_category_link)
    
    crawl_limit -= 1

end = time.time()
print("Time elapsed: ", end - start)
