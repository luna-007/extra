from alpaca.data.live.stock import StockDataStream
from keys import *
from variables import *
import pandas as pd

client = StockDataStream(API_KEY, SECRET_KEY)
streaming_data = pd.DataFrame()

async def quote_handler(quote):
    data = quote.dict()
    data = pd.Series(data)
    # streaming_data = streaming_data.append(data)
    print(data)


client.subscribe_quotes(quote_handler, forex_symbols)
client.run()
