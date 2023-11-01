import os
import requests
import re
import time

# Function to download a page and save it as a .txt file
def save_page_as_txt(url, file_name):
    if (url.find(".css")>=0 or url.find(".js")>=0):
        return
    response = requests.get(url)
    

    if response.status_code == 200:
        # Save the content to a .txt file
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        print(f"Saved page: {url} as {file_name}")
    else:
        print(f"Failed to retrieve page: {url}")


start = time.time()

# Create a directory to store the .txt files
output_directory = "librarything_txt_pages"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Starting URL
start_url = "https://www.librarything.com/"
pages_to_crawl = [start_url]

# Set a limit to the number of pages to crawl to avoid infinite loops
crawl_limit = 100

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
    
    # Extract links from the current page and add them to the pages to crawl
    response = requests.get(current_url)
    if response.status_code == 200:
        #prechadzat categoriami 
        links = re.findall(r'href=["\'](http[s]?://.*?)(?=["\'])', response.text)
        # ci je tam https://bookshop.org/categories/m/
        for link in links:
            if link not in pages_to_crawl:
                pages_to_crawl.append(link)
    
    crawl_limit -= 1

end = time.time()
print("Time elapsed: ",end - start)