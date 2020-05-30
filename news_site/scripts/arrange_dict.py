import pandas as pd
import pickle
from tqdm import tqdm
from newsdb.models import Word
from tqdm import tqdm
import django

def run():
    # file = open('dictionary_final.txt', 'r')

    # lines = file.readlines()

    # ls = []

    # trange = tqdm(lines, total=len(lines))

    # for line in trange:
    #     if line.strip() not in ls:
    #         ls.append(line.strip())

    # with open('dict.pkl', 'wb') as file:
    #     pickle.dump(ls, file)

    ls = None
    with open("dict.pkl", 'rb') as file:
        ls = pickle.load(file)

    for word in tqdm(ls[118041:], total=len(ls[118041:])):
        try:
            if len(word) < 20:
                w = Word(**{'word': word})
                w.save()
            else:
                print(word)
        except django.db.utils.DataError:
            print(word)





