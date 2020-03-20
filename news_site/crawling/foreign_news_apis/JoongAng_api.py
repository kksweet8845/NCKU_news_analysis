# local Django
from newsdb.models import NewsForeign

# third-part
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date

class JoongAngCrawler:
    def __init__ (self):
        self.subjects = {
            '001001': 4,
            '002001': 3,
        }
        self.brand_id = 8

    def get_news_info (self, url = None, sub = None, date = None):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  8,
            'sub_id':    self.subjects[sub],
            'url':     url,
            'title':   self.get_title(soup),
            'content': self.get_content(soup),
            'date':    date,
            'author':  self.get_author(soup),
        }

    def get_news_soup (self, url):
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            return soup.find('h3', class_='articleTit01').get_text()
        except:
            print('error in get_title')
            return None

    def get_date (self, soup):
        try:
            date_string = soup.find('div', class_='articleTit03').get_text().split('|')[1]
            date_string = date_string.split(' ')[1]
            return(str(datetime.strptime(date_string, "%Y.%m.%d").date()))
        except:
            print('error in get_date')

    def get_author (self, soup):
        temp = soup.find('div', class_='articleTit03').get_text().split('|')
        if len(temp) > 1:
            author_string = temp[0].split(' ')[0]
            return author_string
        else:
            return None

    def get_content (self, soup):
        try:
            content = soup.find('div', id='articleBody').get_text()

            return ''.join( content.split() )
        except:
            print('error in get_content')
            return None

    def get_news_headline(self):
        try:
            res = requests.get('https://chinese.joins.com/big5/', timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            
            headline_DOM = soup.select('td#mainCenter div.m1 div.centerTit a')[0]
            href = headline_DOM['href']
            url  = 'https://chinese.joins.com/big5%s' % href[1:]

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
            res = requests.get('https://chinese.joins.com/big5/list.aspx?category=%s&list_type=fl' % sub, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            news_list = soup.find_all('div', class_='a01')

            for news in news_list:
                date_string = news.find('p', class_='a05').get_text().split(' ')[0]
                date_string = str(datetime.strptime(date_string, "%Y.%m.%d").date())

                if date_string == str(datetime.now(timezone).date()):
                    href = news.find('a', class_='a06')['href']
                    url = 'https://chinese.joins.com/big5%s' % href[1:]
                    temp_news = self.get_news_info( url, sub, date = date_string )
                    news_info.append( temp_news )
                else:
                    break

        return news_info

    def getSubjectUrl( self ):
        return ['']

    def insert_news( self, newsList ):
        for news in newsList:
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
            except Exception as e:
                print( e )
        return True
