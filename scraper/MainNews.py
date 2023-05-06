import os
import time
import datetime
from urllib.request import Request, urlopen
import re
import pickle
import pandas
from pygooglenews import GoogleNews
from bs4 import BeautifulSoup
import dateparser
import json


class NewsScraper():
    def __init__(self):
        # Ask the user for the organization's name and initialize some variables
        self.QUERY = input("Enter the organization's name here: ").lower()
        self.CURDIR = str(os.path.dirname(os.path.abspath(__file__)))
        self.SAVEDIR = os.path.join(self.CURDIR, f'{self.QUERY}')
        self.YEAR = str(datetime.date.today().year)
        self.output_dir = os.path.join(self.CURDIR, 'metadata')

        # Create a folder to store metadata if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        # Create a folder to store text data of the organization if it doesn't exist
        if not os.path.exists(self.SAVEDIR):
            os.mkdir(self.SAVEDIR)

    def get_titles(self, search):
        # Use the pygooglenews library to search for news articles
        stories = []
        gn = GoogleNews(lang='en')
        search = gn.search(f'esg news of {search}', from_=str(datetime.date.today() - datetime.timedelta(days=2 * 365)), to_=str(datetime.date.today()))
        newsitems = search['entries']
        for item in newsitems:
            content = {
                'title': item.title,
                'link': item.link
            }
            stories.append(content)
        return stories

    def scraper(self, link):
        # Use the BeautifulSoup library to extract text content from a given link
        try:
            time.sleep(1)
            req = Request(
                url=link,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            webpage = urlopen(req).read()
            soup = BeautifulSoup(webpage, "lxml")
        except:
            print(f"Unable to extract content from {str(link)}")
            pass
        return soup.get_text()

if __name__ == "__main__":
    scraper = NewsScraper()
    gog_news = scraper.get_titles(scraper.QUERY)

    for i in gog_news[:2]:
        try:
            for key in i:
                if key == 'link':
                    # Update the link in the dictionary with the actual URL
                    print("Trying to extract link....")
                    instance = scraper.scraper(i[key])
                    res = re.findall(r"(https?://[^\s]+)", str(instance))
                    i.update({'link': str(res[0])})
        except Exception as e:
            print(e)

    output_dir_news = os.path.join(scraper.output_dir, f'{scraper.QUERY}_esgnews')
    with open(output_dir_news, "wb") as fp:
        # Save the metadata as a pickle file
        pickle.dump(gog_news, fp)
    link_lst = []
    title_lst = []
    content_lst = []

    for idict in gog_news[:5]: 
        try: 
            for key in idict:  
                if key == 'title': 
                    title_lst.append(str(idict[key]))
                    

                elif key == 'link': 
                    print("trying to extract content....") 
                    stuff = scraper.scraper(idict[key])  
                    link_lst.append(str(idict[key]))
                    content_lst.append(stuff) 

        except Exception as e: 
            print(e) 
    # storing it in a dictionary for later use of csv or json conversion
    
    articles = list(zip(title_lst, content_lst))
    articles_list = []
    for title, content in articles:
        articles_dict = {'title':title,'content':content}
        articles_list.append(articles_dict)
    json_str = json.dumps(articles_list)


    temp_dict = {"links":link_lst,"titles":title_lst,"contents":content_lst}
    
    df = pandas.DataFrame(temp_dict) 
    df.to_csv(scraper.SAVEDIR+'/'+scraper.QUERY+'.csv')

    
