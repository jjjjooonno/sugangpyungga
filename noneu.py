from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pandas import DataFrame
import re
import time

dr = webdriver.Chrome('/Users/joono/Downloads/chromedriver')
dr.implicitly_wait(1000)
dr.get('http://everytime.kr/login')

id = ''
password = ''
dr.find_element_by_name('userid').send_keys(id)
dr.find_element_by_name('password').send_keys(password)
dr.find_element_by_xpath('//*[@id="container"]/form/p[3]/input').click()
dr.find_element_by_xpath('//*[@id="menu"]/li[3]/a').click()
dr.find_element_by_name('keyword').send_keys('성균논어')
dr.find_element_by_name('keyword').send_keys(Keys.RETURN)
time.sleep(1)
lectures = []
drt= dr.page_source
soup = BeautifulSoup(drt,'html.parser')
lectures.append(soup.find_all('a',attrs= {'class':'lecture'}))
lectures_url_re = re.compile(r'\/lecture\/view\/[0-9]+')
lectures_url=[]
lectures_url.extend(lectures_url_re.findall(str(lectures[0])))
print(lectures_url)
prof_name = []
feedback = []
lecnum = re.compile('[0-9]+')
for i in lectures_url:
    url = 'http://everytime.kr' + i
    dr.get(url)
    drp = dr.page_source
    soupp = BeautifulSoup(drp,'html.parser')
    prof_name.extend(soupp.select('#container > div.head > div.card.header > p > span'))
    feedback.extend(soupp.find_all('p',attrs={'class':'text'}))
    feedback.extend(lecnum.findall(str(i)))
pick_name = re.compile('[가-힣]+')
pick_text = re.compile(r'[가-힣{3:5}\s\.ㄱ-ㅎㅏ-ㅣ\!a-zA-Z\'\?\,0-9]+')
prof_name_txt = []
feedback_txt = []
for i in prof_name:
    prof_name_txt.extend(pick_name.findall(str(i)))
for j in feedback:
    feedback_txt.extend(pick_text.findall(str(j)))
def remove_values_from_list(the_list, val):
    while val in the_list:
        the_list.remove(val)
remove_values_from_list(feedback_txt,'p class')
remove_values_from_list(feedback_txt,'p')
remove_values_from_list(feedback_txt,'br')
remove_values_from_list(feedback_txt,'text')
print(feedback)
print(prof_name_txt)
print(feedback_txt)
pro_name_df = []
lec_num_df = []
feedback_df = []
lectures_url_idx = 0
for i in feedback_txt:
    if i in lectures_url[lectures_url_idx]:
        lectures_url_idx += 1
    else:
        pro_name_df.append(prof_name_txt[lectures_url_idx])
        feedback_df.append(i)
print(pro_name_df)
print(len(pro_name_df))
print(feedback_df)
print(len(feedback_df))
dt = DataFrame({'professor':pro_name_df,'Feedback':feedback_df})
dt.to_csv('feedback__whole.csv',encoding='utf-8',index=None)
dt.to_csv('feedback_noneu_whole_euc_kr.csv',encoding='euc-kr',index=None)
dr.close()