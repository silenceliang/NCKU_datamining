# -*- coding: utf-8 -*-
# !/usr/bin/python3

# u must to restore doc and encoding as 'utf-8'.

from config import DATA_DIR
import csv
import random


class load():

    def __init__(self):
        self.index2word = {}
        self.word2index = {}


def load_data(dir=DATA_DIR):
    dataSet = []
    l = load()
    with open(dir, 'r', encoding='utf-8') as f:
        for row in list(csv.reader(f))[1:]:
            new_row = []
            for i, item in enumerate(row):
                print(item)
                new_row.append(float(item))
            dataSet.append(new_row)
    return dataSet


def extra_attr(dataSet, col):
    target_attr = []
    for x in dataSet:
        target_attr.append([x[col]])

    return target_attr

def split_data(dataSet, rate=0.2):
    lenth =len(dataSet)
    test_num = int(lenth*0.1)
    shuffle_index = list(range(lenth))
    random.shuffle(shuffle_index)
    dataSet = [x for _, x in sorted(zip(shuffle_index, dataSet))]
    train_data = dataSet[test_num:]
    test_data = dataSet[:test_num]
    return train_data, test_data


