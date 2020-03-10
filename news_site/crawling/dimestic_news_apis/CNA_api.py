# local Django
from newsdb.models import New

# third-party
from bs4 import BeautifulSoup
import requests
import pytz

# standard library
from datetime import datetime, date
import re

class CNACrawler:

    def __init__(self):
        self.subjects = {
            'asoc': 1,
            'aipl': 2,
            'aopl': 3,
            'aie': 4,
            'asc': 4,
            'aspt': 5,
            'acn': 6,
            'ait': 7,
            'ahel': 7,
            'aloc': 7,
        }

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        return {
            'brand_id':  7,
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

    def get_author( self, soup ):
        try:
            paragraph_DOM = soup.find('div', class_='centralContent').find('div', class_='paragraph')
            paragrap_string = paragraph_DOM.find_all('p')[0].get_text()
            author_section = re.search( r'（(.*)記者(.*)）', paragrap_string ).group(2)

            return author_section[0:3]
        except:
            return None

    def get_title (self, soup):
        try:
            title = soup.find('div', class_='centralContent').find('h1').get_text()
            return title
        except:
            return None

    def get_date (self, soup):
        try:
            time_DOM = soup.find('div', class_='centralContent').find('div', class_='updatetime')
            date_string = time_DOM.find('span').get_text()
            return(str(datetime.strptime(date_string, "%Y/%m/%d %H:%M").date()))
        except:
            return None

    def get_content (self, soup):
        try:
            content = soup.find('div', class_='centralContent').find('div', class_='paragraph').get_text()
            return "".join( content.split() )
        except:
            return None

    def get_news_today( self ):
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()

        news_info = []
        for sub in self.subjects:
            is_news_today = True
            for page in range(1, 20):
                res = requests.get(url = 'https://www.cna.com.tw/cna2018api/api/simplelist/categorycode/%s/pageidx/%d/' % (sub, page))
                news_list = res.json()['result']['SimpleItems']

                for news in news_list:
                    if news['IsAd'] == 'N':
                        temp_news = self.get_news_info(news['PageUrl'], sub)
                        if temp_news['date'] == str(datetime.now(timezone).date()):
                            news_info.append( temp_news )
                        else:
                            is_news_today = False
                            break

                if is_news_today == False:
                    break

        return news_info

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
