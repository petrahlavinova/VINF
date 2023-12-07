import os
import requests
import re
import time

# Download and save .txt files with html pages of books
def save_page_as_txt(url, file_name):
    if (url.find(".css")>=0 or url.find(".js")>=0):
        return
    # getting html page
    response = requests.get(url,headers={'User-Agent': "School project on STU FIIT for information retrival (xhlavinova@stuba.sk)"})
    
    # storing html page into file
    if response.status_code == 200:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        print(f"Saved page: {url} as {file_name}")
    else:
        print(f"Failed to retrieve page: {url}")

start = time.time()

# directory to store .txt files
output_directory = "books_txt_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# initialize the pages_to_crawl with main 'https://www.pantarhei.sk/knihy' page
start_url = f"https://www.pantarhei.sk/knihy?_gl=1*u3anf0*_up*MQ..&gclid=CjwKCAjw15eqBhBZEiwAbDomEsV0oz_al3T1JkYmtpVCarIRTIGG0hX2Y_Fxv4klBCEU7_-QVGHebRoCWLEQAvD_BwE"
pages_to_crawl = [start_url]
visited_urls = set()

# getting all book pages(pages_to_crawl) for every category of books
while pages_to_crawl:
    current_url = pages_to_crawl.pop(0)

    # check if the URL has already been visited
    if current_url in visited_urls:
        continue
    
    visited_urls.add(current_url)
    
    if type(current_url) is tuple:
        current_url = current_url[0]
    #print(current_url)
    response = requests.get(current_url,headers={'User-Agent': "School project on STU FIIT for information retrival (xhlavinova@stuba.sk)"})
    #print(response.status_code)
    if response.status_code == 200:

        # pattern that puts a condition to save only urls that have pattern of books on the website
        url_pattern =  r'http[s]?://www\.pantarhei\.sk/(\d+-.+?)'
        match = re.search(url_pattern, current_url)
        if match:
            file_name = os.path.join(output_directory, f"page_{len(visited_urls)}.txt")
            save_page_as_txt(current_url, file_name)
        
        # getting references to categories and books from every url
        ul_content = re.search(r'<ul class="categories-tiles">(.*?)</ul>', response.text, re.DOTALL)
        # adding the categories by regex pattern to a pages_to_crawl
        if ul_content:
            ul_content = ul_content.group(1) 
            main_categories = re.findall(r'<a href="([^"]+)">', ul_content)
            for href in main_categories:
                if href not in pages_to_crawl:
                    #print(href)
                    pages_to_crawl.append(href)
                    ul_content =[]
        # or adding the final page of book to a pages_to_crawl
        else: 
            links = re.findall(r'href=["\'](http[s]?://www\.pantarhei\.sk/(\d+-.+?))(?=["\'])', response.text)
            for link in links:
                if link not in pages_to_crawl:
                    pages_to_crawl.append(link)
                    #print(f"page {link}" )
                    

    

end = time.time()
print("Time elapsed: ",end - start)



