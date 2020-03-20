# local Django
from newsdb.models import NewsForeign

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date
import time

class RFICrawler:

    def __init__(self):
        self.subjects = {
            '中國': 6,
            '港澳台': 6,
            '法國': 3,
            '亞洲': 3,
            '非洲': 3,
            '中東': 3,
            '歐洲': 3,
            '美洲': 3,
            '人權': 7,
            '政治': 2,
            '經貿': 4,
            '社會': 1,
            '生態': 7,
            '科技與文化': 7,
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
            'author':  self.get_author(soup),
        }

    def get_news_soup (self, url):
        res = requests.get(
            url = url,
            timeout = 10,
            headers = {'User-Agent': 'Mozilla/5.0'}
        )
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            title = soup.find('h1', class_='t-content__title a-page-title').get_text()
            return title
        except:
            return None

    def get_date (self, soup):
        try:
            date = soup.find('div', class_='t-content__dates').find('time').get_text().split(' ')[0]
            return(str(datetime.strptime(date, '%d/%m/%Y').date()))
        except:
            return None

    def get_author (self, soup):
        try:
            author = soup.find('a', class_='m-from-author__name').get_text()
            return "".join( author.split() )[:15]
        except:
            print( 'author error' )
            return None

    def get_content (self, soup):
        try:
            content = ''
            content_DOM = soup.find('div', class_='t-content__body').find_all('p')
            for DOM in content_DOM:
                content += DOM.get_text()
            return "".join( content.split() )
        except:
            return None

    def get_news_headline(self):
        try:
            res = requests.get(
                    url = 'http://www.rfi.fr/tw/',
                    timeout = 10,
                    headers = {'User-Agent': 'Mozilla/5.0'}
                )
            soup = BeautifulSoup(res.text, 'lxml')
            
            headline_DOM = soup.select('div.m-item-list-article--main-article a')[0]
            href = headline_DOM['href']
            url  = 'http://www.rfi.fr%s' % href

            print(url)

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

        news_list = []

        for sub in self.subjects:
            res = requests.get(
                    url = 'http://www.rfi.fr/tw/%s/' % sub,
                    timeout = 10,
                    headers = {'User-Agent': 'Mozilla/5.0'}
                )
            soup = BeautifulSoup(res.text, 'lxml')
            articles = soup.find_all('section', class_='t-content__section-pb')
            headline = articles[0]
            news_category_DOM = articles[1].find_all('div', class_='m-item-list-article')

            href = headline.find('div', class_='m-item-list-article').find('a')['href']
            url = 'http://www.rfi.fr/tw%s' % href

            temp_news = self.get_news_info( url, sub )

            if temp_news['date'] == str(datetime.now(timezone).date()):
                news_list.append( temp_news )

            for news_DOM in news_category_DOM:
                href = news_DOM.find('a')['href']
                url = 'http://www.rfi.fr/tw%s' % href
                temp_news = self.get_news_info( url, sub )

                if temp_news['date'] == str(datetime.now(timezone).date()):
                    news_list.append( temp_news )
                else:
                    break

        return news_list

    def get_subject_url( self ):
        return ['https://news.ebc.net.tw/realtime']

    def insert_news( self, news_list ):
        for news in news_list:
            try:
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