#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:24:18 2017

@author: hongchen
"""

import pickle
from random import choice

def trans_title_news(news_dict):
    title_news_dict = {}
    for key, i in news_dict.items():
        title_list = []
        news_list = []
        for j in i:
            title_list.append(j[0])
            news_list.append(j[1])   
        title_news_dict[key] = [title_list,news_list]
    return title_news_dict

def news_dict2txt(dictFilePath):
    with open(dictFilePath, 'rb') as fp:
        news_dict = pickle.load(fp)
        fp.close()
    news_dict = trans_title_news(news_dict)
    news_list = []
    for i in range(len(news_dict.items())-1):
        if list(news_dict.keys())[i] + timedelta(days = 1) == list(news_dict.keys())[i+1]:
            next_day_title_list = list(news_dict.values())[i+1][0]
            for j in list(news_dict.values())[i][1]:
                train_text = "article=<d> <p> <s> "
                news = j.split('.')
                for z in news:
                    train_text = train_text + z + " . </s> <s> "
                train_text = train_text[:-5] + " </p> </d>	abstract=<d> <p> <s> " + choice(next_day_title_list) + " . </s> </p> </d>"
                news_list.append(train_text)
    with open('/Users/hongchen/Downloads/BU2017Spring/CS562/CS562_Project/train_text.txt', 'w') as fp:
        for i in news_list:
            print(i + "\r", file = fp)

def vocal_count(dictFilePath):
    with open(dictFilePath, 'rb') as fp:
        news_dict = pickle.load(fp)
        fp.close()
    vocal_dict = {}
    for i in news_dict.values():
        for j in i:
            words = news = j[1].split(' ')
            for z in words:
                if z not in vocal_dict:
                    vocal_dict[z] = 1
                else:
                    vocal_dict[z] += 1
    with open('/Users/hongchen/Downloads/BU2017Spring/CS562/CS562_Project/vocal.txt', 'w') as fp:
        for i in vocal_dict:
            print(i + " " + str(vocal_dict[i]) + "\r", file = fp)
  
news_dict2txt('/Users/hongchen/Downloads/BU2017Spring/CS562/CS562_Project/news/Facebook_news')
vocal_count('/Users/hongchen/Downloads/BU2017Spring/CS562/CS562_Project/news/Facebook_news')