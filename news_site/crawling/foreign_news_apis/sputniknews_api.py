# local Django
from newsdb.models import NewsForeign

# third-part
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date

class SputniknewsCrawler:
    def __init__ (self):
        self.subjects = {
            'china': 6,
            'russia': 3,
            'russia_china_relations': 3,
            'politics': 3,
            'economics': 4,
            'military': 1,
            'society': 1,
            'sport': 5,
            'science': 7,
        }
        self.brand_id = 7

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        if soup != None:
            return {
                'brand_id':  7,
                'sub_id':    self.subjects[sub],
                'url':     url,
                'title':   self.get_title(soup),
                'content': self.get_content(soup),
                'date':    self.get_date(),
                'author':  None
            }
        else:
            return None

    def get_news_soup (self, url):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            return soup
        except:
            print(url)
            print('error in get single news')
            return None

    def get_title (self, soup):
        try:
            return soup.find('h1', {'itemprop': 'headline'}).get_text()
        except:
            print('error in get_title')
            return None

    def get_date (self):
        try:
            timezone = pytz.timezone('Asia/Taipei')
            return(str(datetime.now(timezone).date()))
        except:
            print('error in get_date')

    def get_content (self, soup):
        try:
            content = soup.find('div', {'itemprop': 'articleBody'}).get_text()
            return ''.join(content.split())
        except:
            print('error in get_content')
            return None

    def get_news_headline(self):
        try:
            res = requests.get('http://big5.sputniknews.cn/#latest-stripe', timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            
            headline_DOM = soup.select('div.l-maincolumn div.b-stories-box div.b-stories-index ul.b-stories__list li.b-story-index div.b-story h2.b-story_title a')[0]
            href = headline_DOM['href']
            url  = 'http://big5.sputniknews.cn%s' % href

            headline_news =  NewsForeign.objects.filter(url = url)[0]
            headline_news.is_headline = 1
            headline_news.save()

            return True
            
        except Exception as e:
            print(e)
            return False

    def get_news_today( self ):
        news_today = True
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).strftime('%Y%m%d')

        news_info = []
        for sub in self.subjects:
            try:
                res = requests.get('http://big5.sputniknews.cn/%s/%s/' % (sub, date_today), timeout=10)
            except:
                print(sub)
                print('error in request news category')
                continue

            soup = BeautifulSoup(res.text, 'lxml')

            news_list = soup.find_all('li', class_='b-plainlist__item')
            for news in news_list:
                try:
                    href = news.find('h2', class_='b-plainlist__title').find('a')['href']
                    url = 'http://big5.sputniknews.cn%s' % href
                    temp_news = self.get_news_info( url, sub )
                    news_info.append( temp_news )
                except:
                    print('error in get news_info')
                    continue

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