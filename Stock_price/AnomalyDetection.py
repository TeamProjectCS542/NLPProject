import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')

def detectAnomaly(filePath):
    df = pd.read_csv(filePath)
    df["Mean"] = df[["Open","High","Low","Close"]].mean(axis=1)
    df["Date"] = pd.to_datetime(df["Date"])

    windowlen = int(6)
    movMean = movingaverage(df['Mean'],windowlen)
    movStd = np.std(movMean)

    lowerLine = movMean - 0.1*movStd
    highLine = movMean + 0.1*movStd
    anomalyIndex = []
    itrList = range(len(movMean)-windowlen/2)
    for i in itrList:
        if math.isnan(movMean[i]) or i<windowlen/2:
            continue
        if df['Mean'][i] < (lowerLine[i]) or df['Mean'][i] > (highLine[i]):
            anomalyIndex.append(i)


    plt.plot_date(df["Date"], movMean, fmt="-",color="purple")
    plt.plot_date(df["Date"], df["Mean"], fmt="r-")
    plt.plot_date(df["Date"][anomalyIndex], df["Mean"][anomalyIndex], color="blue")

    plt.show()

    return df["Date"][anomalyIndex]




print(detectAnomaly("AAPL.csv"))


