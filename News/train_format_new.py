#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:24:18 2017

@author: hongchen
"""

import pickle
from datetime import *
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk import word_tokenize
import re
from nltk.stem.snowball import SnowballStemmer
from random import shuffle

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

def news_dict2txt(NewsPaths, Companys):
    whole_txt = []
    news_list = []
    for i in range(len(Companys)):
        dictFilePath = NewsPaths[i]
        CompanyName = Companys[i]
        print(dictFilePath)
        with open(dictFilePath, 'rb') as fp:
            news_dict = pickle.load(fp)
            fp.close()
        news_dict = trans_title_news(news_dict)
        for i in range(len(news_dict.items())-1):
            if list(news_dict.keys())[i] + timedelta(days = 1) == list(news_dict.keys())[i+1]:
                next_day_title_list = list(news_dict.values())[i+1][0]
                processed_next_day_arti_list = list(news_dict.values())[i+1][1]
                processed_today_arti_list = list(news_dict.values())[i][1]

                next_day_arti_list = []
                today_arti_list = []
                # remove the articles start with "Go to the Reuters home page"
                for todayArt in processed_today_arti_list:
                    if todayArt.startswith("Go to the Reuters home page"):
                        continue
                    else:
                        today_arti_list.append(todayArt)

                if len(today_arti_list) ==0:
                    continue

                for nextArt in processed_next_day_arti_list:
                    if nextArt.startswith("Go to the Reuters home page"):
                        continue
                    else:
                        next_day_arti_list.append(nextArt)

                if len(next_day_arti_list) == 0:
                    continue

                # Add documents similaritiy comparison
                vect = TfidfVectorizer(min_df=1)
                tfidf = vect.fit_transform(today_arti_list+next_day_arti_list)
                similarM = (tfidf * tfidf.T).A

                todayMaxIL, nextMaxIL = [], []
                for todayIndex in range(len(today_arti_list)):
                    similarity = 0
                    ti = 0
                    ni = 0
                    add = False
                    for nextDIndex in range(len(today_arti_list),len(next_day_arti_list)+len(today_arti_list)):
                        if similarM[todayIndex][nextDIndex] > similarity and int(similarM[todayIndex][nextDIndex]) != 1:
                            similarity = similarM[todayIndex][nextDIndex]
                            ti, ni = todayIndex, nextDIndex-len(today_arti_list)
                            add = True
                    if add:
                        todayMaxIL.append(ti)
                        nextMaxIL.append(ni)

                for todayMaxI, nextMaxI in zip(todayMaxIL, nextMaxIL):

                    if "PRESS DIGEST-" in next_day_title_list[nextMaxI] or "PRESS DIGEST -" in next_day_title_list[nextMaxI]:
                        continue

                    #format article
                    train_text = "article=<d> <p> <s> "
                    content = today_arti_list[todayMaxI]
                    if "REVIEW (www.afr.com)" in content:
                        content = content.split("REVIEW (www.afr.com)")[1]

                    news = content.split('.')


                    # print(today_arti_list[todayMaxI])
                    # continue;
                    # breakTag = False
                    for z in news:
                        #text processing
                        if "Compiled for Reuters by Media Monitors" in z:
                            continue
                        if "does not vouch for their accuracy" in z:
                            continue
                        if "REVIEW (www.afr.com)" in z:
                            continue
                        # if "www" in z:
                        #     breakTag = True
                        #     break;
                        z = SnowballStemmer("english").stem(z)
                        z = re.sub('\d', '#', z)
                        z = re.sub(r'\w*\d\w*', '', z).strip()
                        # remove \t
                        z = ' '.join(z.split())

                        train_text = train_text + z + " . </s> <s> "

                        #for calculating fre
                        whole_txt.extend(z+" . ")
                    # if breakTag:
                    #     break;
                    train_text = train_text[:-5] + " <s> "+str(list(news_dict.keys())[i])+"&"+CompanyName+" </s> </p> </d>\tabstract=<d> <p> <s> " + next_day_title_list[nextMaxI] + " . </s> </p> </d>"
                    skip = False

                    for feature in train_text.strip().split('\t'):
                        if len(feature.split('=')) != 2:
                            skip = True
                            break
                    if skip == False:
                        news_list.append(train_text)

    #Slice data into test and train
    shuffle(news_list)
    slice1 = int(len(news_list) * 0.8)
    slice2 = int(len(news_list) * 0.9)
    train_data = news_list[0:slice1]
    test_data = news_list[slice1:slice2]
    valid_data = news_list[slice2: len(news_list)]

    with open('/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/new_train_news', 'w') as fp:
        for i in train_data:
            print(i + "\r", file = fp)
    with open('/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/new_test_news', 'w') as fp:
        for i in test_data:
            print(i + "\r", file = fp)
    with open('/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/new_valid_news', 'w') as fp:
        for i in valid_data:
            print(i + "\r", file = fp)
    return whole_txt;

def vocab_fre(textList):

    wholeNewsStr = ''
    for i in textList:
        wholeNewsStr += i

    freList = nltk.FreqDist(word_tokenize(wholeNewsStr)).items()

    with open('/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/news_vocab', 'w') as vo:
        for l in freList:
            line = (l[0] + ' ' + str(l[1]))
            vo.write(line + '\n')

Companys = ['AAPL','GOOGL', 'GE', 'MSFT', 'FB']
NewsPaths = [
        '/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/Apple_news',
        '/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/Google_news',
        '/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/GE_news',
        '/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/Microsoft_news',
        '/Users/kylemiao/Documents/GitHub/Project/NLPProject/News/Facebook_news'
        ]
wholetxt = news_dict2txt(NewsPaths, Companys)
vocab_fre(wholetxt)
# vocal_count('/Users/hongchen/Downloads/BU2017Spring/CS562/CS562_Project/news/Facebook_news')



# with open('../news/Facebook_news', 'rb') as fp:
#     news_dict = pickle.load(fp)
#     for key, i in news_dict.items():
#         print (news_dict[key][0])
#         print ("---------------------------")
#         print (news_dict[key][1])
#         print ("---------------------------")
#         print (news_dict[key][2])
#         print ("---------------------------")
#         print (news_dict[key][3])
#         break;

