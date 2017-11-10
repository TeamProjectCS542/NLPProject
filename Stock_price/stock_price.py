#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import pandas_datareader.data as web
from pandas import Series, DataFrame

yahoo_stocks = web.DataReader("AAPL", "yahoo", datetime(2012,1,1), datetime(2017,10,30))
yahoo_stocks.to_csv('./yahoo_data.csv')
company_list = ["AAPL","GOOGL","FB","MSFT","GE"]
for i in company_list:
    yahoo_stocks = web.DataReader(i, "yahoo", datetime(2012,1,1), datetime(2017,10,30))
    yahoo_stocks.to_csv(i + ".csv")
