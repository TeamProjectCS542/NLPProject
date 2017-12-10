import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy import stats
from scipy import integrate

threshold_percentile = 1;

def defineKDE(SampleData):
    return stats.gaussian_kde(SampleData)

def detectAnomaly(point, kde):
    percentiles = []
    # for score in scores:
    percentile, err = integrate.quad(kde, -np.inf, point)
    # percentiles.append(percentile*100)
    return (percentile * 100)

data = pd.read_csv('../Stock_price/stockChanging_withAnoTag.csv')
kde = defineKDE(data.ChangingRate)

count = 0
data['Anomaly'] = pd.Series(np.zeros(data.shape[0]), index=data.index)
print(data)
for i in range(data.shape[0]):
    print(i)
    #print(data.ix[i].ChangingRate)
    percentile = detectAnomaly(data.ix[i].ChangingRate, kde)
    if percentile <= threshold_percentile or percentile >= (100-threshold_percentile):
        count = count+1
        data.iloc[pd.Series(i), data.columns.get_loc('Anomaly')] = 1


data.to_csv('../Stock_price/stockChanging_withAnoTag.csv', index=False)
print("done!")


#
# print("done!")
# print(data.)


#Add stock changing file
# def stockChanging(filePath, company):
#     df = pd.read_csv(filePath)
#     df["ChangingRate"] = (df["Close"]-df["Open"])/df["Open"]
#     del df["Open"]
#     del df["High"]
#     del df["Low"]
#     del df["Close"]
#     del df["Adj Close"]
#     del df["Volume"]
#     count_row = df.shape[0]
#     for i in range(count_row):
#         df.loc[i, "Company"] = company
#     return df
#
#
# company_list = ["GOOGL", "FB", "MSFT", "GE"]
# d = stockChanging("AAPL.csv", "AAPL")
# for i in company_list:
#     filePath = i + ".csv"
#     d_new = stockChanging(filePath, i)
#     d = d.append(d_new)
# d.to_csv('./stockChanging_withAnoTag.csv', index=False)







#Old moving average method
# def movingaverage(interval, window_size):
#     window = np.ones(int(window_size))/float(window_size)
#     return np.convolve(interval, window, 'same')
#
# def detectAnomaly(filePath):
#     df = pd.read_csv(filePath)
#     df["Mean"] = df[["Open","High","Low","Close"]].mean(axis=1)
#     df["Date"] = pd.to_datetime(df["Date"])
#
#     windowlen = int(6)
#     movMean = movingaverage(df['Mean'],windowlen)
#     movStd = np.std(movMean)
#
#     lowerLine = movMean - 0.1*movStd
#     highLine = movMean + 0.1*movStd
#     anomalyIndex = []
#     itrList = range(len(movMean)-(int)(windowlen/2))
#     for i in itrList:
#         if math.isnan(movMean[i]) or i<windowlen/2:
#             continue
#         if df['Mean'][i] < (lowerLine[i]) or df['Mean'][i] > (highLine[i]):
#             anomalyIndex.append(i)
#
#
#     plt.plot_date(df["Date"], movMean, fmt="-",color="purple")
#     plt.plot_date(df["Date"], df["Mean"], fmt="r-")
#     plt.plot_date(df["Date"][anomalyIndex], df["Mean"][anomalyIndex], color="blue")
#
#     plt.show()
#
#     return df["Date"][anomalyIndex]
# print(detectAnomaly("AAPL.csv"))


