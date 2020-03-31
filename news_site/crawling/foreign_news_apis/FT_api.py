# local Django
from newsdb.models import NewsForeign

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date
import time

class FTCrawler:
    def __init__ (self):
        self.subjects = {
            'world': 3,
            'economy': 4,
            'markets': 4,
            'business': 4,
            'innovation': 4,
            'management': 4,
            'china': 6,
            'education': 7,
            'opinion': 7,
            'lifestyle': 7
        }
        self.brand_id = 5

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        if soup != None:
            return {
                'brand_id':  5,
                'sub_id':    self.subjects[ sub ],
                'url':     url,
                'title':   self.get_title(soup),
                'content': self.get_content(soup),
                'date':    self.get_date(soup),
                'author':  self.get_author(),
            }
        else: 
            return None

    def get_news_soup (self, url):
        try:
            res = requests.get(
                    url, 
                    timeout=10,
                    verify = False
                )
            soup = BeautifulSoup(res.text, 'lxml')
            return soup
        except:
            return None

    def get_title (self, soup):
        try:
            return soup.find('h1', class_='story-headline').get_text()
        except:
            print('error in get_title')
            return None

    def get_date (self, soup):
        try:
            date_string = soup.find(class_='story-time').get_text()
            date = date_string.split(' ')[0]
            return(str(datetime.strptime(date, "更新於%Y年%m月%d日").date()))
        except:
            print('error in get_date')
            return None

    def get_author (self):
        return None

    def get_content (self, soup):
        try:
            temp = soup.find(id='story-body-container')
            content = ''

            for child in temp.children:
                if child.name == 'p':
                    content += child.get_text()
            return content

        except:
            return None

    def get_news_headline(self):
        try:
            res = requests.get(
                    url = 'https://big5.ftchinese.com/', 
                    timeout=10, 
                    verify = False,
                    headers = {'User-Agent': 'Mozilla/5.0'}
                )
            soup = BeautifulSoup(res.text, 'lxml')
            
            headline_DOM = soup.select('h2.item-headline a.item-headline-link ')[0]
            href = headline_DOM['href']
            url  = 'https://big5.ftchinese.com/%s' % href

            headline_news =  NewsForeign.objects.get(url = url)
            headline_news.is_headline = 1
            headline_news.save()

            return True
            
        except Exception as e:
            print(e)
            return False

    def get_news_today( self ):
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()

        news_info = []
        for sub in self.subjects:
            try:
                newsToday = True
                res = requests.get(
                    'http://big5.ftchinese.com/channel/%s.html' % sub, 
                    timeout=10,
                    verify= False
                )
                soup = BeautifulSoup(res.text, 'lxml')
                news_list  = soup.find_all( 'a', class_='item-headline-link' )

                for news in news_list:
                    try:
                        href = news['href']
                        url = 'http://big5.ftchinese.com%s&exclusive' % href
                        temp_news = self.get_news_info( url, sub )

                        # check whether the news today or not
                        if temp_news['date'] == str(datetime.now(timezone).date()):
                            news_info.append( temp_news )
                        else:
                            break
                    except:
                        continue

            except: 
                continue

        return news_info

    def insert_news( self, news_list ):
        for news in news_list:
            try:
                temp_news = NewsForeign.objects.filter(url = news['url'])
                if len(temp_news) == 0:
                    tmp = NewsForeign(
                        title=news['title'],
                        content=news['content'],
                        author= news['author'],
                        brand_id=news['brand_id'],
                        sub_id= news['sub_id'],
                        date=news['date'],
                        url=news['url'],
                        is_headline= False,
                    )
                    tmp.save()
            except:
                print( news )
        return True
