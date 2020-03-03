# local Django
from newsdb.models import New

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
import time, datetime

class EBCCrawler:
    def __init__ (self):
        self.page_num = 2

    def get_news_info (self, url):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  14,
            'sub_id':    self.get_subject(url),
            'url':     url,
            'title':   self.get_title(soup),
            'content': self.get_content(soup),
            'date':    self.get_date(soup),
            'author':  self.get_author(soup),
        }
    
    def get_news_soup (self, url):
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            temp = soup.select('.fncnews-content')[0]
            title = temp.find_all('h1')[0].get_text()
        except:
            return None
        return title
    
    def get_date (self, soup):
        try:
            temp = soup.select('.info')[0]
            date_string = temp.select('.small-gray-text')[0].get_text()
            date_list = date_string.split(" ")
            date_string = date_list[0]
            return str(datetime.datetime.strptime(date_string, "%Y/%m/%d")).split(" ")[0]
        except:
            return None

    def get_author (self, soup):
        try:
            temp = soup.select('.info')[0]
            date_string = temp.select('.small-gray-text')[0].get_text()
            date_list = date_string.split(" ")
        except:
            print( 'author error' )
            return None
            
        if len(date_list) < 5:
            return None
        else:
            return date_list[4]
    
    def get_subject (self, url):
        temp = url.split("/")
        subject = temp[4]
        if('society' in subject):
            return 1
        elif('politics' in subject):
            return 2
        elif('world' in subject ):
            return 3
        elif('business' in subject):
            return 4
        elif('sport' in subject):
            return 5
        elif('china' in subject):
            return 6
        elif('living' or 'story' or 'travel' in subject):
            return 7
        else:
            return 0
    
    def get_content (self, soup):
        temp = soup.find('span', {"data-reactroot": True})
        temp = temp.find_all('p')
        content = ""
        if len(temp) == 0:
            content = soup.find('span', {"data-reactroot": True}).get_text()
        for node in temp:
            if node.findChild() == None:
                if len(node.get_text()) > 0:
                    content += node.get_text()
                elif node.contents != None and len(node.contents) > 0:
                    print(node.contents[0])
                    content += node.contents
        content = "".join(content.split())
        return content
    
    def get_news (self, news_num = 30, start_page = 1):
        if news_num > 600:
            news_num = 600
        page_num = int((news_num - 1) / 30 + 1)
        news_info = []

        count = 0
        for page in reversed(range(start_page, page_num + start_page)):
            res = requests.get('https://news.ebc.net.tw/Realtime?page=%d' % page, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            news_list_area = soup.select('.news-list-area')[0]
            news_list = news_list_area.select('.white-box')

            # read the news content
            for news in reversed(news_list):
                if 'list-ad' in news['class']:
                    continue
                count += 1
                print(  count )
                news_url = news.find_all('a')[0]['href']
                temp = self.get_news_info(url='https://news.ebc.net.tw%s' % news_url)

                # check the news subject is what we want
                if temp[ 'sub_ID' ] != 0:
                    news_info.append(temp)
        
        return news_info
    
    def get_news_today( self ):
        max_page = 20
        news_today = True
        timezone = pytz.timezone('Asia/Taipei')
        time_today_begin = str(datetime.datetime.now(timezone).date())
        timestamp_today_begin = datetime.datetime.strptime(time_today_begin, "%Y-%m-%d").timestamp()
        news_info = []
        
        for page in range(1, max_page + 1):
            res = requests.get('https://news.ebc.net.tw/Realtime?page=%d' % page, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            news_list_area = soup.select('.news-list-area')[0]
            news_list = news_list_area.select('.white-box')

            # read the news content
            for news in news_list:
                # ad block filter
                if 'list-ad' in news['class']:
                    continue
                
                # get news url
                news_url = news.find_all('a')[0]['href']
                temp = self.get_news_info(url='https://news.ebc.net.tw%s' % news_url)

                # check whether the news today or not
                timestamp_news = datetime.datetime.strptime(temp["date"], "%Y-%m-%d").timestamp()
                if timestamp_news < timestamp_today_begin:
                    news_today = False
                    break
                
                # check the news subject is what we want
                if temp[ 'sub_ID' ] != 0:
                    news_info.append(temp)
            
            if not news_today:
                break
        
        return news_info

    def get_subject_url( self ):
        return ['https://news.ebc.net.tw/realtime']

    def insert_news( self, newsList ):
        for news in newsList:
            try:
                tmp = New(
                    title=news['title'],
                    content=news['content'],
                    author= news['author'],
                    brand_id=news['brand_id'],
                    sub_id= news['sub_id'],
                    date=news['date'],
                    url=news['url']
                )
                tmp.save()
            except: 
                print( news )
        return True