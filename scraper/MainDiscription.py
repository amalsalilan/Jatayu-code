from bs4 import BeautifulSoup
import pandas as pd
import requests
import pandas as pd 
import time

df = pd.read_csv("yfinance.csv") 
symbols = list(df["Symbols"])


# Iterate through the column containing NaN and strings
for index, row in df.iterrows():
    if pd.isna(row['Description']):
        # Get the values from other columns
        sym = row['Symbols']
        try: 
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
            headers = {'User-Agent': user_agent}
            elements=[]
            web_data=requests.get(f"https://finance.yahoo.com/quote/{sym}/profile?p={sym}",headers=headers).text
            soup=BeautifulSoup(web_data,'html.parser')
            summary = soup.find_all('p')
            df.at[index, 'Description']= summary[-2].get_text()
            print(df.at[index, 'Description'])
            time.sleep(1)
        except Exception as e: 
            print(e) 
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
            headers = {'User-Agent': user_agent}
            elements=[]
            web_data=requests.get(f"https://finance.yahoo.com/quote/{sym}/profile?p={sym}",headers=headers).text
            soup=BeautifulSoup(web_data,'html.parser')
            summary = soup.find_all('p')
            df.at[index, 'Description']= summary[-3].get_text()
            print(df.at[index, 'Description'])
            time.sleep(1)
    else:
        # Skip or pass if the value is not NaN or string
        pass

df.to_csv("discyfin.csv",index=False)


# print(summary)
# print(soup.find_next_siblings(class_='TzHB6b cLjAic LMRCfc'))
