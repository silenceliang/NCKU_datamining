#!/usr/bin/python3

from AprioriAlgo.file_utills import file_tool
from AprioriAlgo.parameters import file_name, min_sup, file_name_IBM, file_name_IBM1
import sys, getopt
import time

'''
    ref:
    Liu, B. Z., Improved Apriori Mining Frequent Items
    Algorithm. Application Research of Computers, Vol.29, pp. 475-477, 2012. 
'''

def find_seq_1_itemsets(D, min_sup):

    temp_dict = D

    ''' 做剪枝 '''
    for i in list(D):
        support_ratio = len(D[i]) / file_len

        if support_ratio < min_sup:
            del temp_dict[i]

        else:
            ans_dict[i] = support_ratio
            #print(tuple([i]), ' :', support_ratio)
            # show the tid of every item be count.
            # print(set(temp_dict[i]))
    ''' 做剪枝 '''

    return temp_dict


def apriori(D, min_sup):
    '''

    :param D: re-processing dict type
    :param min_sup: minimum support ratio
    :return: a dict , which type would like { (a,b): 0.2 , (a,c): 0.3 , ... }
    '''

    temp_dict = find_seq_1_itemsets(D, min_sup)
    return_dict = temp_dict

    while any(return_dict):

        d = {}
        key_list = list(temp_dict)
        re_key_list = list(return_dict)
        current_sets = []

        for i in range(0, len(re_key_list)):
            for j in range(0, len(key_list)):

                a = [re_key_list[i]] if not isinstance(re_key_list[i], tuple) else list(re_key_list[i])
                b = [key_list[j]]

                key = set(a) | set(b)

                if len(key) < len(a) + len(b):
                    continue

                elif key not in current_sets:

                    current_sets.append(key)
                    temp_value = set(return_dict[re_key_list[i]]) & set(temp_dict[key_list[j]])
                    support_ratio = len(temp_value) / file_len

                    if support_ratio < min_sup:
                        continue

                    ans_dict[tuple(key)] = support_ratio
                    print(tuple(key), ' :', support_ratio)
                    # show the tid of every item be count.
                    #print(temp_value)
                    d[tuple(key)] = temp_value

                else:
                    continue

        return_dict = d

    return ans_dict


def main():

    global file_len, ans_dict  # global variable
    ans_dict = {}

    '''
        use terminal
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
    f = file_tool(file_name,  header=True)
    file_len = len(f.csv_file)
    init_Dict = f.item_id_dict()
    tStart = time.time()
    ans = apriori(init_Dict, min_sup=min_sup)
    tEnd = time.time()
    print('%fs' % (tEnd - tStart))
    for i in sorted(ans.items(), key=lambda d: d[1], reverse=True):
        print(i)
    '''

    f = file_tool(file_name_IBM, False)
    file_len = len(f.csv_file)
    init_Dict = f.item_id_dict()
    #f.build_csv()
    tStart = time.time()
    apriori(init_Dict, min_sup=min_sup)
    tEnd = time.time()
    print('%fs' % (tEnd - tStart))


if __name__ == '__main__':
    main()

