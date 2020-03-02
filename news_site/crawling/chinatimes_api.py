import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import datetime
from fake_useragent import UserAgent
import mysql.connector

class chinatimes_crawler():
    def __init__(self):
        self.category = ['society/total', 'politic/total', 'world/total', 'money/total', 'sport/total', 'chinese/total', 'life/total']
        self.name = ['社會', '政治', '國際', '財經', '體育', '兩岸', '生活']
        self.df = pd.DataFrame(columns=['title', 'date', 'author', 'content', 'sub_ID', 'brand_ID', 'reference'])
        
        self.mycursor = self.mydb.cursor()
        self.sql = "INSERT INTO news_table (title, content, author, brand_ID, sub_ID, date, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        
        self.subject_dict = {'社會': 1,'政治': 2,'國際':3 ,'財經':4,'體育':5,'兩岸':6,'生活':7}
        self.brand_dict = {'TVBS': 1,'Yahoo': 2,'大紀元':3 ,'三立':4,'上報':5,'中天':6,'中央社':7,'中時電子報': 8,'今日新聞': 9,'公視':10 ,'自由時報':11,'民視新聞':12,'風傳媒':13,
                  '東森ETtoday':14,'新頭殼': 15,'聯合新聞網': 16,'蘋果電子報':17 ,'華視':18, 'chinatimes': 8}
        
    def insert(self):
        val = []
        for i in range(len(self.df)):
            val.append((self.df.title[i], self.df.content[i], self.df.author[i], self.df.brand_ID[i], self.df.sub_ID[i],
                       self.df.date[i], self.df.url[i]))
        
        self.mycursor.executemany(self.sql, val)
        self.mydb.commit()
        
    def get_content(self, url_str, kind, df, timeLimit=True):
        ua = UserAgent()
        headers = {'User-Agent': ua.chrome}
        req = requests.get(url_str, headers=headers)
        if req.status_code != 200:
            print(req.status_code)

        html_doc = req.text
        soup = BeautifulSoup(html_doc, 'html.parser')
        title_str = soup.find('h1').string
        try:
            time_str = soup.find('span', {"class": "date"}).string
        except:
            time_str = f'{datetime.date.today()}'
        time_str = time_str.replace('/', '-')
        # timeToken True means accepts this df
        timeToken = True
        if(timeLimit):
            timeToken = (f'{datetime.date.today()}' == time_str.replace('/','-'))            
        # if timeToken is False, return df
        if(not timeToken):
            return df
        
        author_str = soup.find('div', {"class": "author"}).string
        if author_str == None:
            author_str = soup.find('div', {"class": "author"}).find('a').string
        else:
            author_str = re.sub('[\s,\n]','', author_str)
        
        try:
            content_str = ''
            for data in soup.find('div', {"class": "article-body"}).find_all('p'):
                if data.string != None and re.match('\(中時', data.string) == None:
                    if content_str != '':
                        content_str += '\n'
                    content_str += data.string
        except:
            print('content', content_str, url_str)
        try:
            subjuct_str = ''
            info = soup.findAll("span", {"itemprop": "name"})
            subjuct_str = info[1].text
        except:
            subjuct_str = soup.select('title')[0].text
            subjuct_str = re.sub(' - .{2,5}$', '', subjuct_str)
            subjuct_str = re.sub('.+- ', '', subjuct_str)
        if len(subjuct_str) > 3:
            subjuct_str = '政治'

        df = df.append({'title':title_str, 'date':time_str, 'author':author_str, 'content':content_str, 'sub_ID':str(self.subject_dict[kind]),
                        'brand_ID':str(self.brand_dict['中時電子報']), 'url':url_str}, ignore_index=True)
        return df

    # kind == subject
    def crawler(self, url_str, kind, df, timeLimit=True):
        req = requests.get(url_str)
        if req.status_code != 200:
            print(req.status_code)

        html_doc = req.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        links = []
        index = 0
        # for data in soup.select('a[href*="realtimenews"]'):
        for data in soup.find_all('a', href=re.compile('^/realtimenews/[0-9]+-[0-9]+')):
            index+=1
            if(index%2 == 0):
                links.append('https://www.chinatimes.com' + data.get('href'))
        kind = re.sub(r'/total$', '', kind)
        for link in links:
            df = self.get_content(link, kind, df, timeLimit)
        return df
    
    def getNewsToday(self, maxlen=10, timeLimit=True):
        # target means realtime or politic
        self.df = pd.DataFrame(columns=['title', 'date', 'author', 'content', 'sub_ID', 'brand_ID', 'url'])
        
        for ct_ind in range(len(self.category)):
        # 1~11
            for index in range(1, maxlen+1):
                self.df = self.crawler(f'https://www.chinatimes.com/{self.category[ct_ind]}?page={index}&chdtv', self.name[ct_ind], self.df, timeLimit)
        # self.insert()
        return self.df
                
    def getSubjectUrl(self):
        url_df = pd.DataFrame(columns=['subject', 'url'])
        for i in range(len(self.category)):
            url_df.loc[i] = [self.name[i], f'https://www.chinatimes.com/{self.category[i]}?chdtv']
        return url_df

crawler = chinatimes_crawler()
print( crawler.getNewsToday() )
        