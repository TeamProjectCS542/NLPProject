import datetime
import pickle
with open('./Apple_news', 'rb') as fp:
    fb_dict = pickle.load(fp)
    #print(fb_dict)
    fp.close()
word1 = 'stock'
word2 = 'shares'
remove_list = 'go' and 'to' and 'the' and 'reuters' and 'home' and 'page.'
i = 0
key_list = []
all_key = []
for keys in fb_dict.keys():
    s = fb_dict.get(keys)[0][0] + ' ' + fb_dict.get(keys)[0][1]
    if remove_list not in s.lower().split(" "):
        all_key.append(keys)
        if word1 in s.lower().split(" ") or word2 in s.lower().split(" "):
            i+=1
            key_list.append(keys)
        else:
            continue
fb = []
k = 0
import csv
with open('stockPrice.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Company'] == 'AAPL':
            k+=1
            fb.append(row)
train_list = []
train_dict = {}
from datetime import datetime
m = 0
for j in key_list:
    j = j.strftime('%Y-%m-%d')    
    for k in fb:
        if k['Date'] == j:
            train_dict = k
            train_list.append(train_dict)
            m +=1
result_list = []
for l in range(len(fb)):
    if fb[l] in train_list:#
        result_list.append([fb[l-1]['Mean'],fb[l]['Mean'], 1])
    else:
        result_list.append([fb[l-1]['Mean'],fb[l]['Mean'], 0])
import pandas as pd
df = pd.DataFrame(result_list)
df.to_csv('apple_output.csv',index = False)

import numpy as np
train = int(0.7*len(result_list))
test = int(0.3* len(result_list))
df_train = df.sample(train)
df_test = df.sample(test)
x = df_train.ix[:,0:1]
y = df_train.ix[:,2]
x_test = df_test.ix[:,0:1]
y_true = df_test.ix[:,2]
import sklearn.linear_model as linear_model
logit = linear_model.LogisticRegression()
logit.fit(x, y)
y_pred = logit.predict(x_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logit.score(x_test, y_true)))
