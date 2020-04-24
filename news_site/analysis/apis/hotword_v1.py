from ckiptagger import data_utils, construct_dictionary, WS
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re
import os
from django.conf import settings
from newsdb.models import New, Subject, Brand, Brand_sub, Word_brand, Word, HotWord
from multiprocessing import Pool


util_path = settings.BASE_DIR + '/analysis/apis/utils/ckiptagger'
# news_site/analysis/apis/utils
# /home/nober/git/IKDM/NCKU_news_analysis/news_site/analysis/apis/utils/ckiptagger/data
class Hotword:
    def __init__(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        print(util_path)
        self.WS = WS(util_path+'/data')
        self.stopwords = []
        with open(util_path + '/stopwords.txt', encoding='utf8') as f:
            self.stopwords.extend(f.read().split())
        self.brands = Brand.objects.all()
        self.subs = Subject.objects.all()
        self.dict = Word.objects.all()

    def text_preprocessing(self, raw):
        text = raw['content']
        tmp = re.sub(r'（.+）','', text)
        tmp = re.sub(r'〔.+〕', '', tmp)
        tmp = re.sub(r'[\r\n]', '', tmp)
        tmp = tmp.strip()
        # tmp = tmp.split(' ')
        raw['content'] = tmp
        return raw

    def value_convert(self, raw):
        date = raw['update_time']
        raw['update_time'] = date.strftime('%Y-%m-%d')
        raw['date'] = raw['date'].strftime('%Y-%m-%d')
        return raw

    def fetch_news(self, where):
        """ """
        news = New.objects.filter(*where)
        self.df = pd.DataFrame(
            list(news.values()),
            columns=['id', 'title', 'content', 'author', 'brand_id', 'sub_id', 'date', 'update_time', 'url'])

        self.pre_df = self.df \
            .apply(self.text_preprocessing, axis=1) \
            .apply(self.value_convert, axis=1)

        return self.pre_df.to_json(orient='records')

    def get_hotword(self, universe_num):
        words = self.WS(self.pre_df['content'])
        ll = []
        for i in words:
            if len(i) != 0:
                ll.append(' '.join(word for word in i if word not in self.stopwords))

        vectorizer = TfidfVectorizer()
        try:
            tfidf_vec = vectorizer.fit_transform(ll)
        except ValueError:
            print(ll)

        tfidf_arr = tfidf_vec.toarray()
        sort = np.argsort(tfidf_arr, axis=1)[:, -universe_num:]
        names = vectorizer.get_feature_names()
        keywords = pd.Index(names)[sort].values

        self.pre_df['keywords'] = list(keywords[:])

        return self.pre_df.to_json(orient='records')


    def gen_keyBrand(self):
        keyBrand = {}
        news_T = {
            'title': None,
            'url': None,
            'date': None,
            'sub': None
        }
        for row in self.pre_df.iterrows():
            row = row[1]
            brand_name = self.brands.get(id=row['brand_id']).brand_name
            this_info = {
                'title': row['title'],
                'url': row['url'],
                'date': row['date'],
                'sub': self.subs.get(id=row['sub_id']).sub_name
            }
            for keyword in row['keywords']:
                if keyword not in keyBrand.keys():
                    keyBrand[keyword] = {}
                    keyBrand[keyword][brand_name] = {
                        'news' : [
                            this_info,
                        ],
                        'tally' : 1
                    }
                else:
                    if brand_name not in keyBrand[keyword].keys():
                        keyBrand[keyword][brand_name] = {
                            'news': [
                                this_info,
                            ],
                            'tally': 1
                        }
                    else:
                        keyBrand[keyword][brand_name]['news'].append(this_info)
                        keyBrand[keyword][brand_name]['tally'] += 1

        self.keyBrand = keyBrand
        return keyBrand

    def gen_branKey(self):
        brandKey = {}

        news_T = {
            'title': None,
            'url': None,
            'date': None,
            'sub': None
        }

        def fillKeyword(this, row, this_info):
            for keyword in row['keywords']:
                if keyword not in this.keys():
                    this[keyword] = {
                        'news': [this_info, ],
                        'tally': 1
                    }
                else:
                    this[keyword]['news'].append(this_info)
                    this[keyword]['tally'] += 1

        for row in self.pre_df.iterrows():
            row = row[1]
            brand_name = self.brands.get(id=row['brand_id']).brand_name
            this_info = {
                'title': row['title'],
                'url': row['url'],
                'date': row['date'],
                'sub': self.subs.get(id=row['sub_id']).sub_name
            }
            if brand_name not in brandKey.keys():
                this = brandKey[brand_name] = {}
                fillKeyword(this, row, this_info)
            else:
                this = brandKey[brand_name]
                fillKeyword(this, row, this_info)

        self.brandKey = brandKey
        return brandKey

    def rearrange(self):
        """ """
        keyword_brand = None
        brand_keyword = None

