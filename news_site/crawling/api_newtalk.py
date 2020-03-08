# # local Django
# from newsdb.models import New

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date

class NewtalkCrawler:

    def __init__(self):
        self.subjects = {
            '2/政治': 2,
        }

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  15,
            'sub_id':    self.subjects[sub],
            'url':     url,
            'title':   self.get_title(soup),
            # 'content': self.get_content(soup)[:2000],
            # 'date':    self.get_date(soup),
            # 'author':  self.get_author(soup),
        }

    def get_news_soup (self, url):
        res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'lxml')
        return soup

    def get_title (self, soup):
        try:
            title = soup.find('h1', class_='content_title').get_text()
            return "".join( title.split() )
        except:
            return None

    def get_date (self, soup):
        try:
            date_string = soup.find('div', class_='author').contents[1]
            date_string = "".join( date_string.split() )
            return(str(datetime.strptime(date_string, "%Y年%m月%d日%H:%M:%S").date()))
        except:
            return None

    def get_author (self, soup):
        try:
            author = soup.find('div', class_='author').contents[0].get_text()
            return author
        except:
            return None

    def get_content (self, soup):
        news_DOM = soup.find('div', id='news-info').find('div', class_='editor').find_all('p')
        content = ''
        for DOM in news_DOM:
            content += DOM.get_text()
        return "".join( content.split() )

    def test (self):
        news_list = []
        for sub in self.subjects:
            for page in range(1,2):
                res  = requests.get('https://newtalk.tw/news/subcategory/%s/%d' % (sub, page), timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                soup = BeautifulSoup(res.text, 'lxml')
                news_category_DOM = soup.find_all('div', class_='news_box1')

                for news_DOM in news_category_DOM:
                    url = news_DOM.find('div', class_='news-title').find('a')['href']
                    temp_news = self.get_news_info( url, sub )
                    print( temp_news )

    def get_news_today( self ):
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()

        news_list = []
        for sub in self.subjects:
            is_news_today = True
            for page in range(1,10):
                try:
                    res  = requests.get('https://www.upmedia.mg/news_list.php?currentPage=%d&Type=%s?' % (page, sub), timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
                    res.encoding='GBK'
                    soup = BeautifulSoup(res.text, 'lxml')
                    news_category_DOM = soup.find('div', id='news-list')
                    href = news_category_DOM.find('dl', class_='main').find('a')['href']
                    url = 'https://www.upmedia.mg/%s' % href

                    temp_news = self.get_news_info( url, sub )
                    if temp_news['date'] == str(datetime.now(timezone).date()):
                        news_list.append( temp_news )
                except:
                    temp_news = None
                    print( 'error in get main news' )

                news_category = news_category_DOM.find_all('div', class_='top-dl')
                for news_DOM in news_category:
                    try:
                        href = news_DOM.find('dt').find('a')['href']
                        url = 'https://www.upmedia.mg/%s' % href

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

crawler = NewtalkCrawler()
crawler.test()