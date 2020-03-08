# local Django
from newsdb.models import NewsForeign

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date
import time

class AsahiCrawler:
    def __init__ (self):
        self.subjects = {
            'society': 1,
            'politics_economy': 2,
            'world': 3,
            'business': 4,
            'technology': 7,
        }

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  6,
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
        temp = soup.find('div', class_='Title')
        return temp.find('h1').get_text()

    def get_date (self, soup):
        date_string = soup.find(class_='LastUpdated').get_text()
        return(str(datetime.strptime(date_string, "%B %d, %Y").date()))

    def get_author (self):
        return None

    def get_content (self, soup):
        content = soup.find(class_="ArticleText").get_text()

        return "".join(content.split())

    def get_news_today( self ):
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()

        news_info = []
        for sub in self.subjects:
            news_today = True
            res = requests.get('https://asahichinese-f.com/%s' % sub, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            newsUl = soup.find_all('ul', class_="ListHeadline")

            for ul in newsUl:
                for li in ul.find_all('li'):
                    if li.has_attr('class'):
                        if 'HeadlineTopImage-S' in li[ 'class' ]:
                            continue
                    href = li.find('a')['href']
                    url = 'https://asahichinese-f.com%s' % href
                    temp_news = self.get_news_info( url, sub )

                    # check whether the news today or not
                    if temp_news['date'] == str(datetime.now(timezone).date()):
                        news_info.append( temp_news )
                    else:
                        break

        return news_info

    def getSubjectUrl( self ):
        return ['']

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

