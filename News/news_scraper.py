#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 21:22:51 2017

@author: xinyuli
"""
'''
how to extract data:
    import pickle
    with open('/Users/hongchen/Downloads/BU2017Spring/CS562/CS562_Project/Google_news', 'rb') as fp:
        apple_dict = pickle.load(fp)
        fp.close()
'''

import json
import requests
from bs4 import BeautifulSoup, Comment
import csv
import pandas as pd
import io
import time
import random
import pickle
from datetime import datetime, date, timedelta

user_agent_1 = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
user_agent_2 = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8"
global user_list
user_list = [user_agent_1, user_agent_2]
global news_list
result_dict = {}

def news_scrape(company, start_date_time):
    global news_list
    global user_list
    print(start_date_time)
    if start_date_time == date(2017, 10, 1):
        return 0
    title_article_list = []
    base_url = 'http://www.reuters.com/resources/archive/us/'
    headers = {'User-Agent' : random.choice(user_list)}
    today = str(start_date_time)
    today = today.replace("-", "")
    news_url = base_url + today + ".html"
    r = requests.get(url = news_url,headers = headers).text
    s = BeautifulSoup(r,"lxml")
    target_div = s.find('div',class_="contentBand")
    possible_list = target_div.findAll('a')
    
    for i in possible_list:
        if i.get_text() == 'Next Day':
            pass
        elif i.parent['class'] != "pageNavigation" and i.get_text() not in ['Previous Day', 'Archive Home']:
            title = i.get_text()
            if company in title:
                news_article_html = requests.get(url = i.get('href'),headers = headers).text
                news_article_soup = BeautifulSoup(news_article_html,"lxml")
                news_article_list = news_article_soup.findAll('p')
                news_article_text = ''
                for j in news_article_list:
                    try:
                        if j["class"] == None:
                            pass
                    except:
                        news_article_text += j.get_text()
                title_article = [title, news_article_text]
                title_article_list.append(title_article)
    if title_article_list != []:
        result_dict[start_date_time] = title_article_list
    #time.sleep(random.uniform(5,10))
    '''try:
        news_scrape(company, start_date_time + timedelta(days = 1), end_date_time)
    except KeyboardInterrupt:
        return 0
    except:
        try:
            news_scrape(company, start_date_time + timedelta(days = 2))
        except:
            news_scrape(company, start_date_time + timedelta(days = 3))'''


start_date = date(2012, 1, 1)
end_date = date(2017,1,1)
company = "General Electric"
while(start_date != end_date):
    try:
        news_scrape(company, start_date)
        start_date = start_date + timedelta(days = 1)
    except KeyboardInterrupt:
        break
    except: 
        try:
            news_scrape(company, start_date + timedelta(days = 1))
            start_date = start_date + timedelta(days = 2)
        except:
            news_scrape(company, start_date + timedelta(days = 2))
            start_date = start_date + timedelta(days = 3)
        
with open('./GE_news', 'wb') as fp:
    pickle.dump(result_dict, fp)