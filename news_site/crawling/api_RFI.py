# # local Django
# from newsdb.models import NewsForeign

# third-party
from bs4 import BeautifulSoup
from opencc import OpenCC
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

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        cc = OpenCC('s2t')
        return {
            'brand_id':  1,
            'sub_id':    self.subjects[sub]['sub_id'],
            'url':     url,
            'title':   cc.convert(self.get_title(soup)),
            'content': cc.convert(self.get_content(soup)),
            'date':    self.get_date(url),
            'author':  cc.convert(self.get_author(soup)),
        }
    
    def get_news_soup (self, url):
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            title = soup.find('h1', class_='detailed-article-headline').get_text()
            return title
        except:
            return None
    
    def get_date (self, url):
        try:
            url = url.split('/')
            news_date = date( int(url[4]), int(url[5]), int(url[6])) 
            return(str(news_date))
        except:
            return None

    def get_author (self, soup):
        try:
            author = soup.find('div', class_='source-wrapper').find_all('span', class_= 'sub-area-title')[1].get_text()
            return "".join( author.split() )[:15]
        except:
            print( 'author error' )
            return None
    
    def get_content (self, soup):
        try:
            content = soup.find('div', class_='article-content').get_text()
            return "".join( content.split() )
        except:
            return None
    
    def crawling_news_category ( self ):
        news_list = []

        for sub in self.subjects:
            res = requests.get('http://www.rfi.fr/tw/%E4%B8%AD%E5%9C%8B/', timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            print( soup )
            news_headline = soup.find('div', class_='m-item-list-article')
            print( news_headline )
            href = news_headline.find('a')['href']
            print( href )

            # for news in news_category:
            #     href = news.find('a')['href']
            #     url  = 'https://chinese.aljazeera.net%s' % href
            #     print( url )

            #     temp_news = self.get_news_info( url, sub )
            #     print( temp_news )
            # except: 
            #     print( 'error in crasling news category' )
    
    def get_news_today( self ):
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()

        news_list = []
        for sub in self.subjects:
            is_news_today = True
            for page in range(1, 2):
                try:
                    res = requests.get('https://chinese.aljazeera.net/getsummarypages/%s/%d' % (self.subjects[sub]['sub_url'], page), timeout=10)
                    soup = BeautifulSoup(res.text, 'lxml')
                    news_category = soup.find_all('h2', class_='meta__title')

                    for news in news_category:
                        href = news.find('a')['href']
                        url  = 'https://chinese.aljazeera.net%s' % href
                        temp_news = self.get_news_info( url, sub )

                        if temp_news['date'] == str(datetime.now(timezone).date()):
                            news_list.append( temp_news )
                        else:
                            is_news_today = False
                            break
                    
                    if is_news_today == False:
                        break
                except: 
                    print( 'error in crasling news category' )
        
        return news_list

    def get_subject_url( self ):
        return ['https://news.ebc.net.tw/realtime']

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
            except:
                print( news )
        return True

crawler = RFICrawler()
crawler.crawling_news_category()