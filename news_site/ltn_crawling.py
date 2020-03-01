from newsdb.models import New, Subject, Brand, Brand_sub
from newsdb.serializers import SubjectSerializer
import requests
from bs4 import BeautifulSoup as bs
import json
import os, re
from tqdm import tqdm

class ltn_crawling:
    brand_name = "自由時報"
    brand_url = "https://news.ltn.com.tw/"
    brand_ID = 11
    def __init__(self):
        pass

    def crawl_category(self):
        """
            Crawl category
        It should be used at first.
        """
        category_sub_res = requests.get(self.brand_url)
        category_sub_soup = bs(category_sub_res.content, 'html.parser')
        categories = category_sub_soup.select('div.useMobi > ul > li > a')
        subs = []
        common_subs = Subject.objects.all()
        common_subs = SubjectSerializer(common_subs, many=True)
        print(common_subs.data)
        # for i in categories:
        #     name = i['data-desc']
        #     for j in common_subs.data:
        #         sub_ID = j['sub_ID']
        #         sub_name = j['sub_name']
        #         if sub_name == name:
        #             index_href = i['href']
        #             ajax_href = i['href'].replace("list", "ajax")
        #             subs.append({
        #                 'brand_ID' : self.brand_ID,
        #                 'sub_ID' : sub_ID,
        #                 'index_href' : index_href,
        #                 'ajax_href' : ajax_href
        #             })
        #             break
        # for i in subs:
        #     s = Brand_sub(**i)
        #     s.save()




