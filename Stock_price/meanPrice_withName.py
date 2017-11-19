#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 17:21:37 2017

@author: deborahhe
"""
import pandas as pd

def meanPrice_withName(filePath, company):
    df = pd.read_csv(filePath)
    df["Mean"] = df[["Open","High","Low","Close"]].mean(axis=1)
    del df["Open"]
    del df["High"]
    del df["Low"]
    del df["Close"]
    del df["Adj Close"]
    del df["Volume"]
    count_row = df.shape[0]
    for i in range(count_row):
        df.loc[i, "Company"] = company 
    return df


company_list = ["GOOGL","FB","MSFT","GE", "BABA"]
d = meanPrice_withName("AAPL.csv","AAPL")
for i in company_list:
    filePath = i + ".csv"
    d_new = meanPrice_withName(filePath, i)
    d = d.append(d_new)
    

d.to_csv('./stockPrice.csv', index = False)