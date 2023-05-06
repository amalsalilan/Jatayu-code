import numpy as np 
import pandas as pd
import time
import requests
import datetime
from urllib.request import Request, urlopen
from Crypto.Cipher import AES 
import urllib
import re
import pickle
import pandas
from pygooglenews import GoogleNews
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import dateparser  
import io 
import PyPDF2
import os
import csv

class ScrapeMethods(): 
    def __init__(self, organization_name): 
        self.organization_name = organization_name
        self.year = str(datetime.date.today().year)
        self.current_dir = str(os.path.dirname(os.path.abspath(__file__)))
        self.saved_dir = os.path.join(self.current_dir, f'{self.organization_name}')
        self.output_dir = os.path.join(self.current_dir, 'metadata')
        self.pdflinks = [] 
        self.newslinks = []
        self.pdf_links = []
        self.filtered_links = [] 
        #news csv lists 
        self.link_lst = list() 
        self.title_lst = list() 
        self.content_lst = list() 

        # Create a folder to store metadata if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        # Create a folder to store text data of the organization if it doesn't exist
        if not os.path.exists(self.saved_dir):
            os.mkdir(self.saved_dir)  
        
        if not os.path.exists("summary"): 
            os.mkdir("summary")

    def org_summary(self, orgname): 
        if orgname == "apple": 
            page = requests.get(f"https://en.wikipedia.org/wiki/{orgname[0].upper()}{orgname[1:]}_Inc.")
        else: 
            page = requests.get(f"https://en.wikipedia.org/wiki/{orgname[0].upper()}{orgname[1:]}")

        soup = BeautifulSoup(page.content,'html.parser') 
        d1 = soup.find_all('p')[0].get_text()
        d2 = soup.find_all('p')[1].get_text() 
        text = "".join([d1,d2]) 
        clean_string = re.sub(r'\[[^]]*\]', '', text)
        text_file = open(f"summary/{orgname}.txt","w") 
        n = text_file.write(clean_string) 
        text_file.close()
    
    def save_csv(self,df): 
        dataf = pandas.DataFrame(df) 
        dataf.to_csv(self.saved_dir+"/"+self.organization_name+'.csv')
    
    def get_source(self, url): 
        """requesting the url and returning the response 
        url: this function expects a url as str to be passed"""

        try:
            session = HTMLSession()
            return session.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
    
    def put_metadata(self,flagnews,lst):
        meta_report = os.path.join(self.output_dir, f'{self.organization_name}_esgreport')  
        meta_news = os.path.join(self.output_dir, f'{self.organization_name}_esgnews') 
        if flagnews: 
            with open(meta_news, "wb") as fp: 
                pickle.dump(lst, fp)
        else:  
            with open(meta_news,"wb") as fp: 
                pickle.dump(lst, fp)
            
    def organize_news(self,lst,size=5):  
        for i in lst[:size]: 
            try: 
                for key in i: 
                    if key == "link": 
                        print("Trying to extract link....")
                        instance  = self.scraper(i[key]) 
                        res = re.findall(r"(https?://[^\s]+)", str(instance))
                        i.update({"link": str(res[0])})
            except Exception as e: 
                print(e)
                 
        for idict in lst[:size]: 
            try: 
                for key in idict: 
                    if key == "title": 
                        self.title_lst.append(str(idict[key])) 
                    
                    elif key == "link": 
                        print("trying to extract content") 
                        stuff = self.scraper(idict[key]) 
                        self.link_lst.append(str(idict[key])) 
                        self.content_lst.append(stuff) 
            except Exception as e: 
                print(e)


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

    
    def find_src_links(self): 
        """filters and returns the links that are associated with the query"""
        query = urllib.parse.quote_plus(self.organization_name)
        response = self.get_source("https://www.google.co.uk/search?q="+query+"esg report pdf of the year"+self.year)
        links = list(response.html.absolute_links)

        google_domains =('https://www.google.', 
                            'https://google.', 
                            'https://webcache.googleusercontent.', 
                            'http://webcache.googleusercontent.', 
                            'https://policies.google.',
                            'https://support.google.',
                            'https://maps.google.', 
                            'https://twitter.com/',
                            'https://facebook.com/', 
                            'https://www.instagram.com/',
                            'https://in.pinterest.com/',
                            'https://www.facebook.com/',
                            'https://www.youtube.com/'
                        )

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)

        self.links = links
        return links 
    
    def filter_pdf_links(self, lst): 
        temp = self.find_src_links() 
        
        temp2 = list(filter(lambda i: i.endswith('pdf'), temp))
        temp3 = list(filter(lambda i: re.search(r'esg', i) or re.search(r'sustainability', i) or re.search(r'pdf', i) or
                            re.search(r'report', i) or re.search(rf'{self.organization_name}'), temp2))
        temp4 = list(filter(lambda i: not re.search(r'infographic', i) or not re.search(r'graphic', i) or not re.search(r'nse', i) 
                            or not re.search(r'bse', i) or not re.search(r'bseindia', i) or not re.search(r'nseindia', i), temp3))
        self.pdf_links = temp4
        
        try: 
            avoided_percent_pdf = abs(len(temp) - len(self.pdf_links)) / len(temp)
            avoided_percent_pdf = round(avoided_percent_pdf * 100)
            print(str(avoided_percent_pdf) + "%" + " of links were filtered in pdf") 
        except Exception as e: 
            print(e)
        
        return self.pdf_links 
    
    def extract_pdf_content(self, url): 
        response = requests.get(url)
        time.sleep(1)
        open_pdf_file = io.BytesIO(response.content)
        try: 
            pdf = PyPDF2.PdfReader(open_pdf_file)
            text = [page.extract_text() for page in pdf.pages]
        except Exception as e: 
            print(e)
            text = " "
        return "\n".join(text)  
    
    def organize_save_pdf(self, lst): 
        for link in lst: 
            pdfcontent = self.extract_content(link) 
            link = link.replace('.pdf','') 
            link = link.replace('https://','/')
            link = link.replace('/','') 
            try: 
                with open(self.saved_dir+'/'+str(link)+'impdf.txt', 'w',errors='ignore',encoding='utf-8') as file: 
                    file.write(pdfcontent)
            except Exception as e: 
                print(e) 



class RetriveESGScore(ScrapeMethods):
    def __init__(self, csv_file_path):
        # Read CSV file using pandas and get a list of company names
        self.df = pd.read_csv(csv_file_path)
        self.org_names = list(self.df['Name'])
        self.csv_file_path = csv_file_path 
        self.cmpnyName = ScrapeMethods.organization_name

    def find_company(self, input_str):
        # Use regex to search for the company name in the list
        regex = re.compile(re.escape(input_str), re.IGNORECASE)
        for i, company in enumerate(self.org_names):
            if regex.search(company):
                # If found, return the index of the company and its name
                return i, company
        # If not found, return None
        return None, None 

    def get_other_columns(self, row_number):
        # Unpack the column names
        column_names = ['Name', 'Symbols', 'Total ESG Score', 'Environment Score',
           'Social Score', 'Governance Score', 'Controversy Score',
           'Controversy Assessment']
        _, _, total_esg, environment, social, governance, controversy, assessment = column_names

        # Read the CSV file
        with open(self.csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip the header row
            next(csv_reader)
            # Loop through the rows until we reach the specified row number
            for i, row in enumerate(csv_reader):
                if i == row_number:
                    # Return the other columns' data in a dictionary
                    return {
                        total_esg: row[2],
                        environment: row[3],
                        social: row[4],
                        governance: row[5],
                        controversy: row[6],
                        assessment: row[7]
                    }
        # If the specified row number was not found, return None
        return None  
    
