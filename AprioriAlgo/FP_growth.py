from file_utills import file_tool
from parameters import file_name, min_sup, file_name_IBM, file_name_IBM1
from collections import Counter

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


def countSychroz(node, count, dic):
    if node.label != 'root':
        dic[node] = count
        if node.parent:
            countSychroz(node.parent, count, dic)

def sub_path(node, count):
    list = []
    while node.label != 'root':
        node.count = count
        list.append(node.label)
        node = node.parent
    return list[::-1]



def build_FP(d):
    root = Node('null', None, None)
    for node in d.keys():
        if node.parent.label == 'root':
            root.child[node.label] = node
            node.parent = root

    root.disp()


def main():

    f = file_tool('data/Te.csv', False)
    transaction = f.dict
    init_Dict = f.item_id_dict()
    NodeTable = {}
    label_Node = {}

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
            '''ever show'''
            if stop_Node:
                stop_Node.inc(1)
                next_Node = stop_Node

            else:
                next_Node = Node(item, 1, current_Node)
                next_Node.parent = current_Node
                current_Node.child[item] = next_Node

            path.append(next_Node)
            current_Node = next_Node

            '''Node first appear'''
            if next_Node.label not in NodeTable:
                NodeTable[next_Node.label] = set()
                label_Node[next_Node.label] = set()

            NodeTable[next_Node.label].add(tuple(path))
            label_Node[next_Node.label].add(next_Node)

    '''NodeTable store pattern path
    as Node --> [] path_List '''

    for key, pat_list in NodeTable.items():
        print('item:', key)
        print("*****")
        print(pat_list)
        for i in pat_list:
            for x in i:
                print('pattern: ', x.label, x.count)
            print(".....")
        print("-------------------")
    rootNode.disp()

    ''' Extract suffix patterns of paths to the item i
 Construct its Conditional Pattern Base '''

    for i in freq_List:  # label --> frequency
        current_NodeSet = label_Node[i[0]]  # = contains all sub-Node

        print('\n', i[0])
        for node in current_NodeSet:

            l = sub_path(node.parent, node.count)
            print(l)


if __name__ == '__main__':
    main()

