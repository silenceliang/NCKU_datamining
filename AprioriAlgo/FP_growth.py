from file_utills import file_tool
from parameters import file_name, min_sup, file_name_IBM, file_name_IBM1
import time

class Node(object):

    def __init__(self, label, count, parent_Node):
        self.label = label
        self.count = count
        self.parent_Node = parent_Node
        self.child = {}

    def inc(self, numOccur):
        self.count += numOccur

class FP_Tree(object):

    def __init__(self, Node):
        self.dict = {}
        self.child = {}
        self.Node = Node

    def add_Node(self, Node):
        self.dict[Node.label] = Node


def sortListByfrequency(item_list, freq_dict):

    freq_list = [freq_dict[x] for x in item_list]
    return [x for _, x in sorted(zip(freq_list, item_list), reverse=True)]


def main():

    f = file_tool(file_name_IBM, False)
    file_len = len(f.csv_file)
    transaction = f.dict
    init_Dict = f.item_id_dict()

    # {word} --> frequency(int)
    for i in list(init_Dict):  # item : freq
        init_Dict[i] = len(init_Dict[i])

    # tid --> [ x,y,z ]
    # sort in transaction
    for key, value in transaction.items():
        transaction[key] = sortListByfrequency(transaction[key], init_Dict)

    rootNode = Node('root', None, None)
    fp_tree = FP_Tree(rootNode)
    current_Node = rootNode

    for item_list in transaction.values():

        current_Node = rootNode

        for item in item_list:
            if item in fp_tree.dict:
                new_Node = fp_tree.dict[item]
                new_Node.inc(1)
            else:
                new_Node = Node(item, 1, current_Node)
                fp_tree.add_Node(new_Node)
            current_Node = new_Node



    print('\nInstance: %d\nAttribute: %d\n------------------' % (file_len, len(list(init_Dict))))


if __name__ == '__main__':
    main()

