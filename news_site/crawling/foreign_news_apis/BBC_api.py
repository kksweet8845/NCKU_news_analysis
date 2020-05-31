# local Django
from newsdb.models import NewsForeign

# third-part
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date

class BBCCrawler:
    def __init__ (self):
        self.subjects = {
            'world': 3,
            'business': 4,
            'chinese_news': 6
        }
        self.brand_id = 2

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  2,
            'sub_id':    self.subjects[sub],
            'url':     url,
            'title':   self.get_title(soup),
            'content': self.get_content(soup),
            'date':    self.get_date(soup),
            'author':  self.get_author(),
        }

    def get_news_soup (self, url):
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            return soup.find(class_='story-body__h1').get_text()
        except:
            print('error in get_title')
            return None

    def get_date (self, soup):
        try:
            date_string = soup.find(class_='date date--v2').get_text()
            return(str(datetime.strptime(date_string, "%Y年 %m月 %d日").date()))
        except:
            print('error in get_date')

    def get_author (self):
        return None

    def get_content (self, soup):
        try:
            mediaPlayer = soup.find(id='comp-media-player')
            content = ''

            if( mediaPlayer == None ):
                temp = soup.find(class_='story-body__inner')
                for child in temp.children:
                    if child.name == 'p':
                        content += child.get_text()
            else:
                temp = soup.find(class_='story-body')
                for child in temp.children:
                    if child.name == 'p':
                        content += child.get_text()

            return content
        except:
            print('error in get_content')
            return None

    def get_news_headline(self):
        try:
            res = requests.get('https://www.bbc.com/zhongwen/trad', timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')

            headline_DOM = soup.select('div#comp-top-story-1 div.buzzard div.buzzard-item a')[0]
            href = headline_DOM['href']
            url = 'https://www.bbc.com%s' % href

            headline_news =  NewsForeign.objects.get(url = url)
            headline_news.is_headline = 1
            headline_news.save()

            return True

        except Exception as e:
            print(e)
            return False

    def get_news_today( self ):
        news_today = True
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()

        news_info = []
        for sub in self.subjects:
            news_today = True
            res = requests.get('https://www.bbc.com/zhongwen/trad/%s' % sub, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            newsList = soup.find_all('a', class_="title-link")

            for news in newsList:
                href = news['href']
                url = 'https://www.bbc.com%s' % href
                temp_news = self.get_news_info( url, sub )

                # check whether the news today or not
                if temp_news['date'] == str(datetime.now(timezone).date()):
                    news_info.append( temp_news )
                else:
                    is_news_today = False
                    break

        return news_info

    def getSubjectUrl( self ):
        return ['']

    def insert_news( self, newsList ):
        for news in newsList:
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
