# local Django
from newsdb.models import NewsForeign

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date
import time

class NYTCrawler:
    def __init__ (self):
        self.subjects = {
            'world': 3,
            'business': 4,
            'china': 6 ,
            'education': 7,
            'culture': 7,
        }
        self.brand_id = 3

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  3,
            'sub_id':    self.subjects[sub],
            'url':     url,
            'title':   self.get_title(soup),
            'content': self.get_content(soup)[:2000],
            'date':    self.get_date(soup),
            'author':  self.get_author(soup),
        }

    def get_news_soup (self, url):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            return soup
        except:
            print('error in get_news_soup')
            return None

    def get_title (self, soup):
        try:
            return soup.find(class_='article-header').find('h1').get_text()
        except:
            print('error in get_title')
            return None

    def get_date (self, soup):
        try:
            article_header = soup.find(class_="article-header")
            date_string = article_header.find('time').get_text()

            return(str(datetime.strptime(date_string, "%Y年%m月%d日").date()))
        except:
            print('error in get_date')
            return None

    def get_author (self, soup):
        try:
            article_header = soup.find(class_="article-header")
            return article_header.find('address').get_text()
        except:
            return None

    def get_content (self, soup):
        try:
            articleParagraph = soup.find_all(class_='article-paragraph')
            content = ''
            for article in articleParagraph:
                content += article.get_text()

            return content
        except:
            return None

    def get_news_headline(self):
        try:
            res = requests.get('https://cn.nytimes.com/', timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            
            headline_DOM = soup.select('div#photoSpot div.first div.first div.photoWrapper a')[0]
            href = headline_DOM['href']
            url  = 'https://cn.nytimes.com/%s' % href

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
            res = requests.get('https://cn.nytimes.com/%s/' % sub, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            leaderHref = soup.find('h3', class_="sectionLeadHeader").find('a')['href']
            leaderUrl = 'https://cn.nytimes.com%s' % leaderHref

            temp_news = self.get_news_info( leaderUrl, sub )

            if temp_news['date'] == str(datetime.now(timezone).date()):
                news_info.append( temp_news )

            news_list = soup.find_all('h3', class_='regularSummaryHeadline')
            for news in news_list:
                href = news.find('a')['href']
                url =  'https://cn.nytimes.com%s' % href
                temp = self.get_news_info( url, sub )

                if temp_news['date'] == str(datetime.now(timezone).date()):
                    news_info.append( temp_news )
                else:
                    break

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
            except Exception as e:
                print( e )
                print( news )
        return True
