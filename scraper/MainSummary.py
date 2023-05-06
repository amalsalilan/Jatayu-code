from bs4 import BeautifulSoup
import requests
import re
import os

if not os.path.exists("summary"): 
    os.mkdir("summary")


QUERY = input("Enter the Organization Name: ").lower()

# result = find_src_links(QUERY)
# print(result)

# get URL
if QUERY == "apple": 
    page = requests.get(f"https://en.wikipedia.org/wiki/{QUERY[0].upper()}{QUERY[1:]}_Inc.") 
else: 
    page = requests.get(f"https://en.wikipedia.org/wiki/{QUERY[0].upper()}{QUERY[1:]}")
 
# scrape webpage
soup = BeautifulSoup(page.content, 'html.parser')
 
# display scraped data
d1 = soup.find_all('p')[0].get_text()
d2 = soup.find_all('p')[1].get_text() 
text = "".join([d1,d2]) 
clean_string = re.sub(r'\[[^]]*\]', '', text)
text_file = open(f"summary/{QUERY}.txt","w") 
n = text_file.write(clean_string) 
text_file.close()