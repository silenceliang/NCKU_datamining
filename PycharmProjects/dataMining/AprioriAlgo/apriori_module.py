
from file_utills import file_tool
from parameters import file_name, min_sup,file_name_IBM1
import time
import apyori
'''

    python's apriori-Algo implement with apyori.
    it won't be work if you haven't installed this module by command 'pip install apyori'.

'''

#f = file_tool(file_name_IBM3, header=True)
f = file_tool(file_name_IBM1, header=None)

lis = []

for item in f.dict.values():

    lis.append(list(map(str, item)))

tStart = time.time()
re = list(apriori(lis))
tEnd = time.time()
print('%fs' % (tEnd - tStart))

dict = {}
for i in re:
    #if i[1] >= min_sup:
        dict[i[0]] = i[1]

for i in sorted(dict.items(), key=lambda d: d[1], reverse=True):
    print(i)


