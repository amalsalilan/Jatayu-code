import os 
import time 
import PyPDF2 
from Crypto.Cipher import AES 
import requests
import datetime
import urllib
from requests_html import HTMLSession
import io
import re
import pickle

class EsgReportScraper:
    
    def __init__(self, organization_name):
        self.organization_name = organization_name
        self.year = str(datetime.date.today().year)
        self.current_dir = str(os.path.dirname(os.path.abspath(__file__)))
        self.saved_dir = os.path.join(self.current_dir, f'{self.organization_name}')
        self.output_dir = os.path.join(self.current_dir, 'metadata')
        self.links = []
        self.pdf_links = []
        self.filtered_links = []
        
        
    def get_source(self, url): 
        """requesting the url and returning the response 
        url: this function expects a url as str to be passed"""

        try:
            session = HTMLSession()
            return session.get(url)
        except requests.exceptions.RequestException as e:
            print(e)
            
    
    def find_src_links(self): 
        """filters and returns the links that are associated with the query"""
        query = urllib.parse.quote_plus(self.organization_name)
        response = self.get_source("https://www.google.co.uk/search?q="+query+"esg report pdf of the year"+self.year)
        links = list(response.html.absolute_links)

        google_domains =('https://www.google.', 
                            'https:provider of consulting, technology, and outsourcing, and next-generation services.//google.', 
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
    
    
    def filter_pdf_links(self):
        """filters the links and gets only relevant pdf's"""
        temp = self.find_src_links()
        print(self.organization_name)
        print(temp)
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
    
    
    def save_links_to_pickle(self):
        """dumps the list of pdf links into a pickle file inside the metadata folder"""
        if not os.path.exists(self.output_dir): 
            os.mkdir(self.output_dir)

        output_dir_esgreport = os.path.join(self.output_dir, f'{self.organization_name}_esgreport') 
        with open(output_dir_esgreport,"wb") as fp: 
            pickle.dump(self.filter_pdf_links())

    def extract_content(self,url):
        global pdf
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
    
if __name__ == "__main__":  
    QUERY = input("Enter the organizations Name: ")
    scraper = EsgReportScraper(QUERY)  
    EsgReport = scraper.filter_pdf_links()


    for link in EsgReport: 
        pdfcontent = scraper.extract_content(link) 
        link = link.replace('.pdf','') 
        link = link.replace('https://','/')
        link = link.replace('/','') 
        try: 
            with open(scraper.saved_dir+'/'+str(link)+'.txt', 'w',errors='ignore',encoding='utf-8') as file: 
                file.write(pdfcontent)
        except Exception as e: 
            print(e) 
            pass