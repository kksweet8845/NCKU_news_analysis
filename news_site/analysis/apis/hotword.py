from ckiptagger import data_utils, construct_dictionary, WS
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import os


util_path = '../utils/ckiptagger'

class hotword():
    def __init__(self):
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        self.ws = WS(util_path+'/data', disable_cuda=False)
        self.stopwords = []
        with open(util_path+'/stopwords.txt' , encoding = 'utf8') as f:
            self.stopwords.extend(f.read().split())

    def origin_x(self):
        self.df['content'] = self.df['content'].apply(lambda x: x.replace('\n',''))
        words = self.ws(self.df['content'])
        ll = []
        for i in words:
            ll.append(' '.join([word for word in i if word not in self.stopwords]))
        return ll

    # return a dictionary
    def getHotWords(self, df, hots_num=20, universe_num=50):
        self.df = df
        baseline_data = {
            'x': self.origin_x()
        }

        #TF-IDF
        vectorizer = TfidfVectorizer()
        tfidf_vec = vectorizer.fit_transform(baseline_data['x'])
        #numpy to list
        tfidf_arr = tfidf_vec.toarray()

        #sort && get the bigger score words
        sort = np.argsort(tfidf_arr, axis=1)[:, -universe_num:]
        names = vectorizer.get_feature_names()
        keyWords = pd.Index(names)[sort].values

        #puts into the df
        self.df['keywords'] = list(keyWords[:])

        # count words appear times -- seperate subject
        hots = {}
        for i in range(1,8):
            hots[i] = {}

        for i in range(len(self.df)):
            for word in self.df.iloc[i].keywords:
                if f'{word}' not in hots[self.df.iloc[i].sub_ID]:
                    hots[self.df.iloc[i].sub_ID][f'{word}'] = 1
                else:
                    hots[self.df.iloc[i].sub_ID][f'{word}'] += 1
        # sort hots by value -- seperate subject
        for i in range(1,8):
            hots[i] = {k: v for k, v in sorted(hots[i].items(), key=lambda item: item[1], reverse=True)}

        # get top word -- seperate subject
        self.today_hotkeys = {}
        for i in range(1,8):
            self.today_hotkeys[i] = []
        for i in range(1,8):
            it_dic = iter(hots[i])
            for j in range(hots_num):
                try:
                    self.today_hotkeys[i].append(next(it_dic))
                except:
                    pass

        return self.today_hotkeys