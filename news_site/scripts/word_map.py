from django.shortcuts import render
from analysis.apis import Hotword, WordMap
from django.db.models import Q
import json
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm
import numpy as np
from datetime import datetime, timedelta
import re

def wordmap():
    """ """
    wp = WordMap()
    word_dict = []
    # for i in tqdm(range(maxid // scale)):
    #     data = wp.fetch_news([Q(id__gt=i*scale) & Q(id__lt=(i+1)*scale -1),])
    #     word_dict.append(wp.gen_dict(data))

    pre_df = wp.fetch_news([Q(id__gt=0),])
    total = len(pre_df)
    bin = 200
    trange = tqdm(range(0, len(pre_df), 200))

    for i in trange:
        j = i + 200
        if len(pre_df) < j:
            j = len(pre_df)
        words = wp.gen_dict(pre_df[i:j])
        with open('dictionary.txt', 'a') as file:
            for dw in words:
                file.write(f"{dw}\n")
    return True


def run():

    i = 0
    ll = []
    pbar = tqdm(total=2000000)
    with open('dictionary.txt', 'r') as file:
        while(1):
            word = file.readline()
            if word != '\n' or word != '':
                word = re.sub(f'[\n]', '', word)
                ll.append(word)
            if word == '':
                break
            if pbar.n % 10000 == 0:
                ll = np.unique(np.array(ll)).tolist()
            pbar.update(1)
    ll = np.unique(np.array(ll)).tolist()
    with open('dictionary_final.txt', 'w') as file:
        for l in ll:
            file.write(f"{l}\n")
    print(len(ll))