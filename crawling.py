import os
import requests
import re
import time

# Download and save .txt file
def save_page_as_txt(url, file_name):
    if (url.find(".css")>=0 or url.find(".js")>=0):
        return
    response = requests.get(url,headers={'User-Agent': "School project on STU FIIT for information retrival (xhlavinova@stuba.sk)"})
    
    if response.status_code == 200:
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(response.text)
        
        print(f"Saved page: {url} as {file_name}")
    else:
        print(f"Failed to retrieve page: {url}")

start = time.time()

# Directory to store .txt files
output_directory = "books_txt_files"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)


start_url = f"https://www.pantarhei.sk/knihy?_gl=1*u3anf0*_up*MQ..&gclid=CjwKCAjw15eqBhBZEiwAbDomEsV0oz_al3T1JkYmtpVCarIRTIGG0hX2Y_Fxv4klBCEU7_-QVGHebRoCWLEQAvD_BwE"
pages_to_crawl = [start_url]
visited_urls = set()

while pages_to_crawl:
    current_url = pages_to_crawl.pop(0)

    # Check if the URL has already been visited
    if current_url in visited_urls:
        continue
    
    visited_urls.add(current_url)
    
    if type(current_url) is tuple:
        current_url = current_url[0]
    #print(current_url)
    response = requests.get(current_url,headers={'User-Agent': "School project on STU FIIT for information retrival (xhlavinova@stuba.sk)"})
    #print(response.status_code)
    if response.status_code == 200:

        url_pattern =  r'http[s]?://www\.pantarhei\.sk/(\d+-.+?)'

        match = re.search(url_pattern, current_url)
        if match:
            file_name = os.path.join(output_directory, f"page_{len(visited_urls)}.txt")
            save_page_as_txt(current_url, file_name)
        
        ul_content = re.search(r'<ul class="categories-tiles">(.*?)</ul>', response.text, re.DOTALL)

        if ul_content:
            ul_content = ul_content.group(1) 
            main_categories = re.findall(r'<a href="([^"]+)">', ul_content)
            for href in main_categories:
                if href not in pages_to_crawl:
                    #print(href)
                    pages_to_crawl.append(href)
                    ul_content =[]
        else: 
            links = re.findall(r'href=["\'](http[s]?://www\.pantarhei\.sk/(\d+-.+?))(?=["\'])', response.text)
            for link in links:
                if link not in pages_to_crawl:
                    pages_to_crawl.append(link)
                    #print(f"page {link}" )
                    

    

end = time.time()
print("Time elapsed: ",end - start)



