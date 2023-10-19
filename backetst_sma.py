import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

gold = yf.Ticker('GC=F')

data = gold.history('5y')

data['SMA_60'] = data.iloc[:,1].rolling(window=60).mean()

data = data.iloc[59:]


dates = []
signals = []

data.reset_index(inplace = True)

flag = True

for row in range(len(data.index)):
    
    if data.iloc[row]['SMA_60'] > data.iloc[row]['Close'] and flag == True:
        flag = False
        dates.append(pd.Timestamp(data.iloc[row]['Date']))
        signals.append('Buy')
        
        
    elif data.iloc[row]['SMA_60'] < data.iloc[row]['Close'] and flag == False:
        flag = True
        dates.append(pd.Timestamp(data.iloc[row]['Date']))
        signals.append('Sell')
        
frame = pd.DataFrame(signals, columns=['Signal'])
frames = pd.DataFrame(dates, columns=['Date'])

result = pd.concat([frame, frames], axis = 1) 
# result.set_index('Dates', inplace=True)

value = pd.merge(data, result, 'outer',on='Date')

print(value[value['Signal'].notnull()])
# ax = plt.gca()
        
# data.plot(kind='line', y = 'Open', ax = ax)
# data.plot(kind = 'line', y = 'SMA_60', color = 'red', ax= ax)
# plt.show()