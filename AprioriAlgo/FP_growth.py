from file_utills import file_tool
from parameters import file_name, min_sup, file_name_IBM, file_name_IBM1
import time

class Node(object):

    def __init__(self, label, count, parent):
        self.label = label
        self.count = count
        self.parent = parent
        self.child = {}

    def add_count(self, count):
        self.count += count

    def show(self, ind=1):
        print('  ' * ind, self.label, ' ', self.count)
        for child in self.child.values():
            child.show(ind + 1)

    def find(self, item):

        if item in self.child:
            return self.child[item]
        else:
            for child in self.child.values():
                child.find(item)
        return None

    def filter(self, limit, label, current_pattern, F_dict):  # [frozenset(),frozenset(),]

        if self.child:
            for item in self.child.values():
                if item.count < limit:
                    continue
                else:
                    F_dict[frozenset([label, item.label])] = item.count
                    current_pattern.append(item.label)  # [node.label, item.label]
                    F_dict[frozenset(current_pattern)] = item.count
                    item.filter(limit, label, current_pattern, F_dict)


def sortListByfrequency(item_list, freq_dict):

    freq_list = [freq_dict[x] for x in item_list]
    return [x for _, x in sorted(zip(freq_list, item_list), reverse=True)]


def sub_path(node, count):

    list = []
    if node:
        while node.label != 'root':
            list.append(tuple([node.label, count]))
            node = node.parent

    return list[::-1]


def build_FP(root, path):

    current_Node = root
    for item in path:
        stop_Node = current_Node.find(item[0])
        '''ever show'''
        if stop_Node:
            stop_Node.add_count(stop_Node.count)
            next_Node = stop_Node

        else:
            next_Node = Node(item[0], item[1], current_Node)
            next_Node.parent = current_Node
            current_Node.child[item[0]] = next_Node

        current_Node = next_Node


def obtain_Pattern(root, minsup, label):

    F_dict = {}
    children = root.child.values()
    if children:
        for node in children:  # root下的父點
            if node.count < minsup:
                continue
            else:
                if frozenset([label, node.label]) in F_dict:
                    F_dict[frozenset([label, node.label])] = F_dict[frozenset([label, node.label])] + node.count
                else:
                    F_dict[frozenset([label, node.label])] = node.count

                node.filter(minsup, label, [label, node.label], F_dict)

    return F_dict

def main():
    global file_len

    f = file_tool(file_name, True)
    file_len = len(f.csv_file)
    min_sup_n = min_sup * file_len

    transaction = f.dict
    init_Dict = f.item_id_dict()
    NodeTable = {}
    label_Node = {}

    tStart = time.time()
    ''' build frequency Table '''
    # {word} --> frequency(int)
    for i in list(init_Dict):  # item : freq
        init_Dict[i] = len(init_Dict[i])

    ''' sort frequency Table '''
    # sort dict by frequency , output a list
    freq_List = sorted(init_Dict.items(), key=lambda d: d[1], reverse=False)

    ''' sort transaction  '''
    # tid --> [ x,y,z ]
    for key, value in transaction.items():
        transaction[key] = sortListByfrequency(transaction[key], init_Dict)

    ''' build main FP-Tree '''
    rootNode = Node('root', None, None)
    init_Dict['root'] = 0

    for item_list in transaction.values():
        current_Node = rootNode
        path = []
        for item in item_list:
            stop_Node = current_Node.find(item)
            '''ever show'''
            if stop_Node:
                stop_Node.add_count(1)
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

    #rootNode.show()

    ans_dict = {}

    ''' Extract suffix patterns of paths to the item i
 Construct its Conditional Pattern Base '''
    for i in freq_List:  # label --> frequency

        label = i[0]
        current_NodeSet = label_Node[label]  # = contains all sub-Node
        root = Node('null', None, None)

        for node in current_NodeSet:
            path = sub_path(node.parent, node.count)
            #print(node.label, path)
            build_FP(root, path)

        #root.disp()  # show sub-tree
        # root.show()  # show sub-tree

        final_dict = obtain_Pattern(root, min_sup_n, label)
        ans_dict.update(final_dict)

        ''' add unit '''
        ans_dict[frozenset([label])] = i[1]

        #for x, j in final_dict.items():
        #    print(x, j)

    for i, j in ans_dict.items():
        print(i, j)

    tEnd = time.time()
    print('%fs' % (tEnd - tStart))


if __name__ == '__main__':
    main()

