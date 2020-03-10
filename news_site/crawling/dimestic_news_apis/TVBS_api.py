# local Django
from newsdb.models import New

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date

class TVBSCrawler:

    def __init__(self):
        self.subjects = {
            'local': 1,
            'politics': 2,
            'world':3,
            'sports':5,
            'life': 7,
            'focus': 7,
        }

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  1,
            'sub_id':    self.subjects[sub],
            'url':     url,
            'title':   self.get_title(soup),
            'content': self.get_content(soup)[:2000],
            'date':    self.get_date(soup),
            'author':  self.get_author(soup),
        }
    
    def get_news_soup (self, url):
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            title = soup.find('h1', class_='margin_b20').get_text()
            return "".join( title.split() )
        except:
            return None
    
    def get_date (self, soup):
        try:
            time_string = soup.find('div', class_='title').find('div', class_='time').get_text()
            date_string = time_string.split(" ")[0]
            return(str(datetime.strptime(date_string, "%Y/%m/%d").date()))
        except:
            return None

    def get_author (self, soup):
        try:
            author = soup.find('div', class_='title').find('h4').find('a').get_text()
            return author
        except:
            return None
    
    def get_content (self, soup):
        try:
            content = soup.find('div', id='news_detail_div').get_text()
            return "".join( content.split() )
        except:
            return None
    
    def get_news_today( self ):
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()

        news_list = []
        for sub in self.subjects:
            try:
                res = requests.get('https://news.tvbs.com.tw/%s' % sub, timeout=10)
                soup = BeautifulSoup(res.text, 'lxml')
                news_category = soup.find('ul', id='block_pc').find_all('li')

                for news in news_category:
                    href = news.find('a')['href']
                    url  = 'https://news.tvbs.com.tw%s' % href

                    temp_news = self.get_news_info( url, sub )

                    if temp_news['date'] == str(datetime.now(timezone).date()):
                        news_list.append( temp_news )
                    else:
                        is_news_today = False
                        break
            except: 
                print( 'error in crasling news category' )
        
        return news_list

    def insert_news( self, newsList ):
        for news in newsList:
            try:
                tmp = New(
                    title=news['title'],
                    content= news['content'],
                    author= news['author'],
                    brand_id=news['brand_id'],
                    sub_id= news['sub_id'],
                    date=news['date'],
                    url=news['url'],
                )
                tmp.save()
            except Exception as e:
                print( e )
        return True