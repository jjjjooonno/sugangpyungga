from pandas import *
import re
dt1 = read_csv('feedback_inseung_gojeun_whole.csv')
cl1 = []
for i in range(0,len(dt1['Feedback'])):
    cl1.append('gojeun')
dt1['class'] = cl1
dt2= read_csv('feedback_noneu_whole.csv')
cl2 = []
for j in range(0,len(dt2['Feedback'])):
    cl2.append('noneu')
dt2['class'] = cl2
dt = concat([dt1,dt2],axis = 0,ignore_index=True)
dt = DataFrame(dt)
a=[]
import time
# # re.compile(r'^이 정보를 확인하기 위해')
for k in range(0,len(dt['Feedback'])):
    if '이 정보를 확인하기 위해' in dt['Feedback'][k]:
        a.append(k)
time.sleep(3)
for i in a:
    dt = dt.drop(i,axis=0)
dt.to_csv('concat2.csv')
print(dt[850:870])
print(dt.tail())
