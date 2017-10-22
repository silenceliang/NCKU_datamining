#!/usr/bin/python3

from file_utills import file_tool
from parameters import file_name, min_sup, file_name_IBM, file_name_IBM1
import sys, getopt
import time


def find_seq_1_itemsets(D, min_sup):

    temp_dict = D

    for i in list(D):

        support_ratio = len(D[i]) / file_len
        if support_ratio < min_sup:
            del temp_dict[i]

        else:
            ans_dict[i] = support_ratio

    return temp_dict


def apriori(D, min_sup):
    '''
    :param D: re-processing dict type
    :param min_sup: minimum support ratio
    :return: a dict , which type would like { {a,b}: tid , {a,c}: tid , ... }
    '''

    temp_dict = find_seq_1_itemsets(D, min_sup)
    return_dict = temp_dict
    before_duplicate_set = set()  # the last be pruned

    while any(return_dict):

        print('Size of set of large itemsets: %d' % len(list(return_dict)))
        return_dict_tmp = {}  # every time I go to another table
        re_key_set = set(return_dict)
        candidate_set = re_key_set
        duplicate_set = set()  # current be pruned

        for i in re_key_set:  # changed set
            candidate_set = candidate_set.difference({i})
            for j in candidate_set:  # only one element {x}

                #  in case of new set contain duplicated set
                if len(before_duplicate_set) > 0:
                    if i.difference(j).issubset(before_duplicate_set) | \
                            len(i.difference(j).intersection(j.difference(i))) == 0:
                        continue

                key = i | j
                temp_value = return_dict[i] & return_dict[j]

                before_counts = len(return_dict[i])
                current_counts = len(temp_value)  # count items

                confidence_ratio = current_counts / before_counts
                support_ratio = current_counts / file_len  # min support

                if support_ratio < min_sup:
                    duplicate_set.add(key)
                else:
                    ans_dict[key] = support_ratio
                    # show the count, support, conf.
                    # print(key, ' :', current_counts, (support_ratio, confidence_ratio))
                    # show the tid of every item be count.
                    # print(temp_value)
                    return_dict_tmp[key] = temp_value

        # start from (x,y) to duplicate
        before_duplicate_set = duplicate_set
        return_dict = return_dict_tmp

    return ans_dict


def main():

    global ans_dict ,file_len # global variable
    ans_dict = {}

    '''
        use in terminal
    try:
        INPUT, _ = getopt.getopt(sys.argv[1:], "i:m:")
        file, min_sup = INPUT

        global file_len, ans_dict  # global variable
        f = file_tool(file[1], header=True)
        file_len = len(f.csv_file)
        init_Dict = f.rev_dict
        ans_dict = {}
        apriori(init_Dict, min_sup=float(min_sup[1]))


    except getopt.GetoptError as e:
        print(str(e))
        print("Usage: %s -i input_.csv -m min_sup[0,1]" % sys.argv[0])
        sys.exit(2)

    '''

    '''  
    # for kaggle dataSet:

    f = file_tool(file_name,  header=True)
    file_len = len(f.csv_file)
    init_Dict = f.item_id_dict()
    for i in init_Dict:
        init_Dict[i] = frozenset(init_Dict[i])

    tStart = time.time()
    ans = apriori(init_Dict, min_sup=min_sup)
    tEnd = time.time()
    print('%fs' % (tEnd - tStart))
    for i in sorted(ans.items(), key=lambda d: d[1], reverse=True):
        print(i)

    '''
# for IBM dataSet:

    f = file_tool(file_name_IBM, False)
    file_len = len(f.csv_file)
    init_Dict = f.item_id_dict()
    #f.build_csv()
    for i in init_Dict:
        init_Dict[i] = frozenset(init_Dict[i])

    print('\nInstance: %d\nAttribute: %d\n------------------' % (file_len, len(list(init_Dict))))

    tStart = time.time()
    apriori(init_Dict, min_sup=min_sup)
    tEnd = time.time()
    print('%fs' % (tEnd - tStart))


if __name__ == '__main__':
    main()
