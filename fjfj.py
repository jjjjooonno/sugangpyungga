from konlpy.tag import Mecab
from pandas import *
mecab = Mecab()
dt = read_csv('concat.csv')
a = dt['professor'].unique()
a = list(a)
b=[]
countdic = {}
for i in a:
    b.append([])

for j in range(0,len(dt['Feedback'])):
    idx = a.index(dt['professor'][j])
    b[idx].extend(mecab.nouns(str(dt['Feedback'][j])))
for k in b:
    for word in k:
        count = countdic.get(word, 0)
        countdic[word] = count + 1
import operator
countdic_sort = sorted(countdic.items(), key=operator.itemgetter(1),reverse = True)
print(countdic_sort[:30])
word = []
c = []
for l in range(0,len(countdic_sort)):
    word.append(countdic_sort[l][0])
    c.append(countdic_sort[l][1])
dtt = DataFrame({'word':word,'count':c})
print(dtt[:5])
dtt.to_csv('word_count.csv')

