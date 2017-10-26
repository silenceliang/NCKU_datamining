from file_utills import file_tool
from parameters import file_name, min_sup, file_name_IBM, file_name_IBM1
from collections import defaultdict

class Node(object):

    def __init__(self, label, count, parent):
        self.label = label
        self.count = count
        self.parent = parent
        self.child = {}

    def inc(self, count):
        self.count += count

    def disp(self, ind=1):
        print('  ' * ind, self.label, ' ', self.count)
        for child in self.child.values():
            child.disp(ind + 1)

    def find(self, item):

        if item in self.child:
            return self.child[item]
        else:
            for child in self.child.values():
                child.find(item)
        return None




def sortListByfrequency(item_list, freq_dict):

    freq_list = [freq_dict[x] for x in item_list]
    return [x for _, x in sorted(zip(freq_list, item_list), reverse=True)]

def pattern_combine(patern_list):
    d = {}
    for NodeSet in patern_list:
        for x in NodeSet:
            if x not in d: d[x] = 1
            else: d[x] += 1
    print(d)


def main():

    f = file_tool('data/Te.csv', False)
    file_len = len(f.csv_file)
    transaction = f.dict
    init_Dict = f.item_id_dict()
    NodeTable = {}

    # {word} --> frequency(int)
    for i in list(init_Dict):  # item : freq
        init_Dict[i] = len(init_Dict[i])

    # sort dict by frequency , output a list
    freq_List = sorted(init_Dict.items(), key=lambda d: d[1], reverse=False)

    # tid --> [ x,y,z ]
    # sort in transaction
    for key, value in transaction.items():
        transaction[key] = sortListByfrequency(transaction[key], init_Dict)

    rootNode = Node('root', None, None)
    init_Dict['root'] = 0

    # build Tree
    for item_list in transaction.values():
        current_Node = rootNode
        path = []
        for item in item_list:
            stop_Node = current_Node.find(item)

            if stop_Node:
                stop_Node.inc(1)
                next_Node = stop_Node

            else:
                next_Node = Node(item, 1, current_Node)
                next_Node.parent = current_Node
                current_Node.child[item] = next_Node

            current_Node = next_Node

            if next_Node.parent.label != 'root':
                path.append(next_Node.parent)

            if next_Node.label not in NodeTable:
                NodeTable[next_Node.label] = set()

            NodeTable[next_Node.label].add(frozenset(path))


    for key, pat_list in NodeTable.items():
        print('item:', key)
        print("*****")
        # pattern_combine(pat_list)

        for i in pat_list:
            for x in i:
                print('pattern: ', x.label, x.count)
        print(".....")
        print("-------------------")
    rootNode.disp()


    print('\nInstance: %d\nAttribute: %d\n------------------' % (file_len, len(list(init_Dict))))


if __name__ == '__main__':
    main()

