import pandas as pd
import pickle
from tqdm import tqdm


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





