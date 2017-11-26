# -*- coding: utf-8 -*-
# !/usr/bin/python3

import math
from config import DATA_DIR
import feature_select as fs
import load

def E_distance(data1, data2, length):
    dis = 0
    for x in range(length):
        dis += pow((data1[x] - data2[x]), 2)
    return math.sqrt(dis)

def neighbors(train_data, test_instance, k):
    length = len(test_instance)
    for train_instance in train_data:
        E_distance(train_instance, test_instance, length)
    pass


def main():
    print("load data from {} ...".format(DATA_DIR))
    dataSet = load.load_data(DATA_DIR)
    print("split to trainData and testData ...")
    train, test = load.split_data(dataSet, rate=0.1)
    print("trainData size = {}\ntestData size = {}".format(len(train), len(test)))
    fs.Extra_tree(train, load.extra_attr(train, 12))


if __name__ == '__main__':
    main()
