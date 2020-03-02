import requests
from bs4 import BeautifulSoup
# import mysql.connector
import time, datetime, pytz

class WebCrawler:
    def __init__(self):
        # self.cnx = mysql.connector.connect(user='root', database='SETN')
        self.sub_ID = 0

    def getNewsInfo(self, url):
        soup = self.getNewsSoup(url)
        temp = {
            'brand_ID':  4,
            'sub_ID':  self.getSubject(url),
            'url':     url,
            'title':   self.getTitle(soup, url),
            'content': self.getContent(soup),
            'date':    self.getDate(soup),
            'author':  self.getAuthor(soup),
        }
        return temp

    def getNewsSoup(self, url):
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        return soup

    def getTitle(self, soup, url):
        if( soup.find('h1', class_='news-title-3') == None ):
            print( url )
            return ''
        title = soup.find('h1', class_='news-title-3').text
        return title
    
    def getDate(self, soup):
        date = soup.find('time', class_='page-date').text
        return date

    def getAuthor(self, soup):
        author = soup.find('span', class_='reporter')
        if not author.text:
            author = soup.find('p').text
        else:
            author = author.text
        return author[:15]

    def getContent(self, soup):
        content_join = ''
        article = soup.find('article')
        contents = article.find_all('p')
        author = soup.find('span', class_='reporter')
        if author.text:
            for content in contents:
                content_join += content.text
        else:
            flag = 0
            for content in contents:
                if flag > 0:
                    content_join += content.text
                flag = 1
        return content_join[:2000]
    
    def getSubjectUrl(self):
        
        return ['https://www.setn.com/ViewAll.aspx?PageGroupID=41', 
                'https://www.setn.com/ViewAll.aspx?PageGroupID=6',
                'https://www.setn.com/ViewAll.aspx?PageGroupID=5',
                'https://www.setn.com/ViewAll.aspx?PageGroupID=2',
                'https://www.setn.com/ViewAll.aspx?PageGroupID=34',
                'https://www.setn.com/ViewAll.aspx?PageGroupID=4']

    # def insertSubjectUrl(self, url):
    #     for i in range(6):
    #         url = self.getSubjectUrl()[i]
    #         subject = self.getSubject(url)
    #         cursor = self.cnx.cursor()
    #         sql = "INSERT INTO brands_sub(brand_ID, sub_ID, index_href, ajax_href) VALUES(%s, %s, %s, %s)"
    #         val = ('4', str(subject), url, url + '&p=1')
    #         cursor.execute(sql, val)
    #         self.cnx.commit()

    #     if(cursor.rowcount > 0):
    #         return True
    #     else:
    #         return False
    
    def getSubject(self, url):
        if(self.sub_ID==0):
            return 1
        elif(self.sub_ID==1):
            return 2
        elif(self.sub_ID==2):
            return 3
        elif(self.sub_ID==3):
            return 4
        elif(self.sub_ID==4):
            return 5
        elif(self.sub_ID==5):
            return 7
        else:
            return 0
    
    def getNews(self, url):
        news_info = []
        for i in range(6):
            url = self.getSubjectUrl()[i]
            self.sub_ID = i
            for page in range(10):
                res = requests.get(url + '&page=%d'% (page+1))
                soup = BeautifulSoup(res.content, 'html.parser')
                news_list_area = soup.find_all('h3', class_='view-li-title')
                for news in news_list_area:
                    news_url = news.find('a')['href']
                    temp = self.getNewsInfo(url = 'https://www.setn.com%s' % news_url)
                    news_info.append(temp)
        
        return news_info
    

    def getNewsToday(self, url):
        timezone = pytz.timezone('Asia/Taipei')
        news_today = True
        time_today_begin = str(datetime.datetime.now(timezone).date())
        timestamp_today_begin = datetime.datetime.strptime(time_today_begin, "%Y-%m-%d").timestamp()
        news_info = []
        for i in range(6):
            url = self.getSubjectUrl()[i]
            self.sub_ID = i
            for page in range(1):
                res = requests.get(url + '&page=%d'% (page+1))
                soup = BeautifulSoup(res.content, 'html.parser')
                news_list_area = soup.find_all('h3', class_='view-li-title')
                for news in news_list_area:
                    news_url = news.find('a')['href']
                    temp = self.getNewsInfo(url = 'https://www.setn.com%s' % news_url)
                    news_info.append(temp)
                    timestamp_news = datetime.datetime.strptime(temp["date"], "%Y/%m/%d %H:%M:%S").timestamp()

                    if timestamp_news < timestamp_today_begin:
                        news_today = False
                        break
            
                if not news_today:
                    break
        
        return news_info

    # def insertNews(self, newsList):
    #     cursor = self.cnx.cursor()
    #     sql = "INSERT INTO news(title, content, author, brand_ID, subject, date, url) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    #     val = [(news['title'], news['content'], news['author'], str(news['brand_ID']), str(news['sub_ID']), news['date'], news['url'] ) for news in newsList]
    #     cursor.executemany(sql, val)
    #     self.cnx.commit()

    #     if(cursor.rowcount > 0):
    #         return True
    #     else:
    #         return False

web_Crawler = WebCrawler()
get_subject_url = web_Crawler.getSubjectUrl()
# a = web_Crawler.insertSubjectUrl(get_subject_url)
get_news_today = web_Crawler.getNewsToday(get_subject_url)
# b = web_Crawler.insertNews(get_news_today)
print( get_news_today )
