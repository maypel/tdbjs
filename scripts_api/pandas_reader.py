import datetime as dt
import pandas as pd
import yfinance as yf 
from pandas_datareader import data as pdr



end = dt.datetime.now()
start = dt.datetime(2024,1,1)

yf.pdr_override()
df = pdr.get_data_yahoo('BTC-USD', start, end)
df.head()
