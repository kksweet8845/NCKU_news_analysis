# local Django
from newsdb.models import NewsForeign

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date
import re

class EpochTimesCrawler:

    def __init__(self):
        self.subjects = {
            'news413': 6,
            'news412': 3,
            'news418': 3,
            'news415': 6,
            'news414': 6,
            'news994': 1,
            'news403': 5,
            'news420': 4,
            'news2008': 7,
        }

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  10,
            'sub_id':    self.subjects[sub],
            'url':     url,
            'title':   self.get_title(soup),
            'content': self.get_content(soup)[:2000],
            'date':    self.get_date(soup),
            'author':  self.get_author(soup),
        }

    def get_news_soup (self, url):
        res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            title = soup.find('h1', class_='title').get_text()
            return "".join( title.split() )
        except:
            return None

    def get_date (self, soup):
        try:
            header_DOM = soup.find('div', id='artbody')
            date_string = header_DOM.find('time')['datetime']
            return(str(datetime.strptime(date_string.split('T')[0], "%Y-%m-%d").date()))
        except:
            return None

    def get_author (self, soup):
        try:
            content_DOM = soup.find('div', id='artbody')
            author_string = content_DOM.find_all('p')[0].get_text()
            author = re.search(r'(.*)記者(.*)綜合報導', author_string).group(2)
            return author
        except:
            return None

    def get_content (self, soup):
        news_DOM = soup.find('div', id='artbody').contents
        content = ''
        for DOM in news_DOM:
            if DOM.name == 'p':
                content += DOM.get_text()
        return "".join( content.split() )

    def get_news_headline(self):
        try:
            res  = requests.get('https://www.epochtimes.com/b5/n24hr.htm', timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            soup = BeautifulSoup(res.text, 'lxml')       
            
            headline_DOM = soup.select('div#leftcol div.topbox div.left a')[0]
            url = headline_DOM['href']

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
            is_news_today = True
            for page in range(1, 20):
                try:
                    res  = requests.get('https://www.epochtimes.com/b5/%s_%d.htm' % (sub, page), timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                    soup = BeautifulSoup(res.text, 'lxml')
                    news_category_DOM = soup.find('div', class_='topbox').find('div', class_='arttitle')
                    url = news_category_DOM.find('a')['href']

                    temp_news = self.get_news_info( url, sub )

                    if temp_news['date'] == str(datetime.now(timezone).date()):
                        news_list.append( temp_news )
                except:
                    temp_news = None
                    print( 'error in get main news' )

                news_category = soup.find('div', id='artlist').find_all('div', class_='posts')
                for news_DOM in news_category:
                    try:
                        url = news_DOM.find('div', class_='arttitle').find('a')['href']

                        temp_news = self.get_news_info( url, sub )
                        if temp_news['date'] == str(datetime.now(timezone).date()):
                            news_list.append( temp_news )
                        else:
                            is_news_today = False
                            break
                    except:
                        temp_news = None
                        print( 'error in get news category' )

                if is_news_today == False:
                    break
        return news_list

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
                print( news )
        return True