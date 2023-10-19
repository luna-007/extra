import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pyfolio as pf


aapl_hist = pd.read_pickle('aapl_hist.pkl')
aapl_hist.drop(['Dividends', 'Stock Splits', 'Volume'], axis = 1, inplace=True)

aapl_hist.reset_index(inplace=True)
aapl_hist['Date'] = aapl_hist['Date'].dt.tz_localize(None)
aapl_hist['SMA'] = aapl_hist['Close'].rolling(256).mean()
aapl_hist = aapl_hist[257:]
aapl_hist.reset_index(inplace=True)
aapl_hist['returns'] = aapl_hist['Close'].pct_change() 

aapl_hist['P'] = aapl_hist['Close'].pct_change().add(1).fillna(1).cumprod()*1000

def signal_generate(data):
    position = []
    buy_price = []
    sell_price = []
    market = False

    for i in range(len(aapl_hist)):
        if data['Close'][i] > data['SMA'][i]:
            if market == False:
                position.append(1.0)
                buy_price.append(data['Close'][i])
                sell_price.append(np.nan)
                market = True
            elif market == True:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                position.append(0.0)
        elif data['Close'][i] < data['SMA'][i]:
            if market == True:
                position.append(-1.0)
                sell_price.append(data['Close'][i])
                buy_price.append(np.nan)
                market = False
            elif market == False:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                position.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
    return pd.Series([position, buy_price, sell_price])
            
aapl_hist['signal'], aapl_hist['buy_price'], aapl_hist['sell_price'] = signal_generate(aapl_hist)

aapl_hist['strategy'] = aapl_hist['signal'] * aapl_hist['returns']

plt.subplots(figsize=(16, 10))
plt.plot(aapl_hist['Close'], label='Close', color='blue', alpha=0.35)
plt.plot(aapl_hist['SMA'], label='SMA', color='orange', alpha=0.35)
plt.scatter(aapl_hist.index,aapl_hist['sell_price'], color='red', alpha=0.35, label='Sell')
plt.scatter(aapl_hist.index,aapl_hist['buy_price'], color='green', alpha=0.35, label='Buy')
plt.margins(x=0.005, y=0.005)
plt.legend(loc='upper left')
plt.show()