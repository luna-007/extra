from alpaca.data.requests import StockBarsRequest
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.timeframe import TimeFrame
from keys import *
from variables import *
import datetime as dt
start = dt.datetime(2022, 1, 1)
end = dt.datetime(2023, 9, 18)


def cleanData(data):
    data.reset_index(inplace=True)
    data.drop(['symbol', 'vwap', 'trade_count'],axis=1, inplace=True)
    return data


client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

hist_req = StockBarsRequest(
    symbol_or_symbols=symbols,
    timeframe=TimeFrame.Day, 
    start= start, 
    end= end
    )

data = client.get_stock_bars(hist_req).df
data = cleanData(data)

data['sma'] = data['close'].rolling(120).mean().fillna(0, inplace=False)

DATA = data
