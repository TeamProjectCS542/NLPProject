#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 19:24:18 2017

@author: hongchen
"""

import pickle

def news_dict2txt(dictFilePath):
    with open(dictFilePath, 'rb') as fp:
        news_dict = pickle.load(fp)
        fp.close()
    news_list = []
    for i in news_dict.values():
        for j in i:
            train_text = "article=<d> <p> <s> "
            news = j[1].split('.')
            #remove the articles start with "Go to the Reuters home page"
            if news[0] == "Go to the Reuters home page":
                continue
            for z in news:
                #remove \t
                z = ' '.join(z.split())
                train_text = train_text + z + " . </s> <s> "
            #Add the \t symbol
            train_text = train_text[:-5] + " </p> </d>\tabstract=<d> <p> <s> " + j[0] + " . </s> </p> </d>"
            skip = False
            for feature in train_text.strip().split('\t'):
                if len(feature.split('=')) != 2:
                    skip = True
                    break
            if skip == False:
                news_list.append(train_text)
    with open('../News/news_train', 'w') as fp:
        for i in news_list:
            print(i + "\r", file = fp)

# def vocal_count(dictFilePath):
#     with open(dictFilePath, 'rb') as fp:
#         news_dict = fp.read().split('\r')#pickle.load(fp)
#         fp.close()
#     vocal_dict = {}
#     for i in news_dict.values():
#         for j in i:
#             words = news = j[1].split(' ')
#             for z in words:
#                 if z not in vocal_dict:
#                     vocal_dict[z] = 1
#                 else:
#                     vocal_dict[z] += 1
#     with open('../News/news_vocab', 'w') as fp:
#         for i in vocal_dict:
#             print(i + " " + str(vocal_dict[i]) + "\r", file = fp)

def vocab_fre(filePath):
    with open(filePath, 'rb') as fp:
        news_dict = pickle.load(fp)

    wholeNewsStr = ''
    for i in news_dict.values():
        for j in i:
            wholeNewsStr += j[0] + ' ' + j[1]
    import nltk
    from nltk import word_tokenize
    freList = nltk.FreqDist(word_tokenize(wholeNewsStr)).items()

    with open('../News/news_vocab', 'w') as vo:
        for l in freList:
            line = (l[0] + ' ' + str(l[1]))
            vo.write(line + '\n')

    
# news_dict2txt('../news/Facebook_news')
# vocal_count('../news/Facebook_news')
vocab_fre('../News/Facebook_news')
