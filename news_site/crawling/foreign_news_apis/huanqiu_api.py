# local Django
from newsdb.models import NewsForeign

# third-party
from bs4 import BeautifulSoup
from opencc import OpenCC
import requests
import pytz

# standard library
from datetime import datetime, date
from string import Template

class HuanqiuCrawler:
    def __init__ (self):
        self.subjects = {
            'finance': {
                'sub_id': 4,
                'sub_url': Template('https://finance.huanqiu.com/api/list?node=%22/e3pmh1hmp/e3pmh1iab%22,%22/e3pmh1hmp/e3pn46htn%22,%22/e3pmh1hmp/e3pn60gdi%22,%22/e3pmh1hmp/e3pn60gdi/e3pn60h31%22,%22/e3pmh1hmp/e3pn60gdi/e3pru2fi2%22,%22/e3pmh1hmp/e3pn60rs2%22,%22/e3pmh1hmp/e3pn60rs2/e3pn60skq%22,%22/e3pmh1hmp/e3pn60rs2/e3ptlr015%22,%22/e3pmh1hmp/e3pn61831%22,%22/e3pmh1hmp/e3pn61an9%22,%22/e3pmh1hmp/e3pn61chp%22,%22/e3pmh1hmp/e3pn62ihu%22,%22/e3pmh1hmp/e3pn62uuq%22,%22/e3pmh1hmp/e3pn6314j%22,%22/e3pmh1hmp/e3pn6314j/e3pn6323a%22,%22/e3pmh1hmp/e3pn6314j/e3ptma9ah%22,%22/e3pmh1hmp/e3ptkencb%22,%22/e3pmh1hmp/e3ptlrdc9%22,%22/e3pmh1hmp/e3ptlrdc9/e3ptltkc2%22,%22/e3pmh1hmp/e3ptlrdc9/e3ptm2ci2%22,%22/e3pmh1hmp/e7i6qafud%22,%22/e3pmh1hmp/e7i6t8c0j%22,%22/e3pmh1hmp/e7lipkhq1%22,%22/e3pmh1hmp/e7lipkhq1/e7lipkii0%22,%22/e3pmh1hmp/e7lipkhq1/e7o08h1r8%22&offset=$offset&limit=$limit')
            },
            'china': {
                'sub_id': 6,
                'sub_url': Template('https://china.huanqiu.com/api/list?node=%22/e3pmh1nnq/e3pmh1obd%22,%22/e3pmh1nnq/e3pn61c2g%22,%22/e3pmh1nnq/e3pn6eiep%22,%22/e3pmh1nnq/e3pra70uk%22,%22/e3pmh1nnq/e5anm31jb%22,%22/e3pmh1nnq/e7tl4e309%22&offset=$offset&limit=$limit')
            },
            'sports': {
                'sub_id': 5,
                'sub_url': Template('https://sports.huanqiu.com/api/list?node=%22/e3pmh3jvm/e3pn4vk37%22,%22/e3pmh3jvm/e3pn4vk37/e3pn61aah%22,%22/e3pmh3jvm/e3pn4vk37/e3pn62b3q%22,%22/e3pmh3jvm/e3pn4vk37/e3pn638jv%22,%22/e3pmh3jvm/e3pn4vk37/e3pn669vr%22,%22/e3pmh3jvm/e3pn4vk37/e82e6tcpo%22,%22/e3pmh3jvm/e3pn61psg%22,%22/e3pmh3jvm/e3pn61psg/e3pn61qfv%22,%22/e3pmh3jvm/e3pn61psg/e7tn9k8oi%22,%22/e3pmh3jvm/e3pn61psg/e7tn9o6uo%22,%22/e3pmh3jvm/e3pn61psg/e7tn9rf8b%22,%22/e3pmh3jvm/e3pn61psg/e7tna015g%22,%22/e3pmh3jvm/e3pn62e6c%22,%22/e3pmh3jvm/e3pn62e6c/e3pn62euk%22,%22/e3pmh3jvm/e3pn62e6c/e3prbvcgu%22,%22/e3pmh3jvm/e3pn62e6c/e82e138l9%22,%22/e3pmh3jvm/e3pn7fhub%22,%22/e3pmh3jvm/e3pn7fhub/e3pn7fif4%22,%22/e3pmh3jvm/e80lb2feu%22&offset=$offset&limit=$limit')
            },
            'world': {
                'sub_id': 3,
                'sub_url': Template('https://world.huanqiu.com/api/list?node=%22/e3pmh22ph/e3pmh2398%22,%22/e3pmh22ph/e3pmh26vv%22,%22/e3pmh22ph/e3pn6efsl%22&offset=$offset&limit=$limit')
            },
        }

    def get_news_info (self, url, sub):
        soup = self.get_news_soup(url)
        cc = OpenCC('s2t')
        if soup != None:
            return {
                'brand_id':  9,
                'sub_id':    self.subjects[sub]['sub_id'],
                'url':     url,
                'title':   cc.convert(self.get_title(soup)),
                'content': cc.convert(self.get_content(soup))[:2000],
                'date':    self.get_date(soup),
                'author':  self.get_author(soup),
            }
        else:
            return None

    def get_news_soup (self, url):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'lxml')
            return soup
        except:
            return None

    def get_title (self, soup):
        try:
            return soup.find(class_='t-container-title').find('h3').get_text()
        except:
            return None

    def get_date (self, soup):
        try:
            articleHeader = soup.find(class_="metadata-info")
            dateString = articleHeader.find('p', class_='time').get_text()
            date = dateString.split(" ")[0]

            return(str(datetime.strptime(date, "%Y-%m-%d").date()))
        except:
            return None

    def get_author (self, soup):
        try:
            articleHeader = soup.find(class_="metadata-info")
            authorString = articleHeader.find('span', class_='author').get_text()
            return None
        except:
            return None

    def get_content (self, soup):
        try:
            content = soup.find('section', {'data-type':'rtext'}).get_text()
            return ''.join(content.split())
        except:
            print('error in get_content')
            return None

    def get_news_today( self ):
        timezone = pytz.timezone('Asia/Taipei')
        date_today = datetime.now(timezone).date()
        limit = 20

        news_info = []
        for sub in self.subjects:
            print(sub)
            is_news_today = True

            for count in range(10):
                try:
                    res = requests.get(self.subjects[sub]['sub_url'].substitute(offset = str(count*limit), limit = str(limit)), timeout=10)
                    news_list = res.json()['list']
                except:
                    continue

                for news in news_list:
                    if 'title' in news:
                        try:
                            url = 'https://%s.huanqiu.com/article/%s' % ( sub, news['aid'] )
                            temp_news = self.get_news_info( url, sub )

                            # check whether the news today or not
                            if temp_news['date'] == str(datetime.now(timezone).date()):
                                news_info.append( temp_news )
                            else:
                                is_news_today = False
                                break
                        except:
                            print('error in get single news info')
                            continue

                if is_news_today == False:
                    break

        return news_info

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

