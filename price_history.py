from keys import *
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical.stock import StockHistoricalDataClient
from datetime import datetime

client = StockHistoricalDataClient(
    api_key=API_KEY,
    secret_key=SECRET_KEY
)
def get_price_hist(stock, start: datetime, end: datetime):
    """
    This will work when symbol string or list of symbol strings is provided
    """
    
    request_params = StockBarsRequest(
        symbol_or_symbols=stock,
        timeframe = TimeFrame.Day,
        start= start,
        end= end
    )
    
    stock_hist = client.get_stock_bars(request_params) 

    return stock_hist

aapl_hist = get_price_hist('AAPL', start=datetime(2020,1,1), end=datetime(2023,5,1))

print(aapl_hist.df)