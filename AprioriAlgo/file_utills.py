
import pandas as pd

class file_tool(object):
    '''
        just do pre-processing task.
        you can jump out here if it isn't interesting to you.
    '''
    def __init__(self, file_name, header):
        ''' deal wth raw csv.'''
        self.unique = set()

        if header:
            self.csv_file = pd.read_csv(file_name, encoding='utf-8')
            self.csv_head = list(self.csv_file)

            ''' deal wth content of raw csv.'''
            self.id = self.csv_file[self.csv_head[0]]
            self.items = [self.get_CSV_col(x) for x in self.csv_head][1:]

            self.dict = self.id_item_dict()

        else:
            self.csv_file = pd.read_csv(file_name, encoding='utf-8', header=None)
            self.dict = {}
            for i in range(0, len(self.csv_file)):
                temp = []

                for x in self.csv_file.iloc[i]:
                    if not str(x) == 'nan':
                        self.unique = self.unique | {str(x)}
                        temp.append(frozenset([x]))
                self.dict[i] = temp

            self.rev_dict = self.item_id_dict()

        ''' create dict.'''
        #self.dict = self.id_item_dict()
        #self.rev_dict = self.item_id_dict()

    def get_CSV_col(self, attr_col):
        re_list = []
        for i in self.csv_file[attr_col]:
                re_list.append('%s:%s' % (attr_col, i))

        return re_list

    def id_item_dict(self):

        dict = {}
        for n, id in enumerate(self.id):
            item_list = []
            for i in range(0, len(self.items)):
                item_list.append(self.items[i][n])

            dict[id] = item_list

        return dict

    def item_id_dict(self):

        dict = {}
        for key, value in self.dict.items():
            for string in value:
                dict.setdefault(string, []).append(key)

        return dict

    ''' 用來轉成weka .csv格式 '''
    def build_csv(self):

        cab = list(self.unique)

        hd = len(cab)  # 寬
        length = len(self.csv_file)  # 長

        big_list = []
        for i in range(0, length):
            temp = ['' for i in range(0, hd)]
            for k in self.dict[i]:
                for n, j in enumerate(cab):
                    if j == str(k):
                         temp[n] = 'T'

            big_list.append(temp)

        cab = ['item=%s' % i for i in cab]

        df = pd.DataFrame(columns=range(0, hd))
        for i in range(0, length):
            df.loc[i] = big_list[i]

        df.to_csv('feed_weka195.csv', sep=',', encoding='utf-8', index=False)
