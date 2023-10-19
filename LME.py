import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import pandas_ta as ta

data = pd.read_csv("Data.csv")


# start = dt.date(2015, 1, 1)
# end = dt.date(2023, 5, 1)

# data = yf.download("MSFT", start, end)

def smaCalc(data, n: int):
    data.ta.sma(close = "Close",length= n, append=True)

def calcRSI(data):
    data.ta.rsi(close = "Close",length = 14, append = True)

smaCalc(data, 20)
calcRSI(data)

# print(data)
# fileName = "Data.csv"
# data.index = pd.to_datetime(data.index, format='%d/%m/%y', errors='ignore')
# data.to_csv(fileName)

plt.margins(x=0, y=0)
plt.xlabel("Date")
plt.ylabel("Price")
plt.title("MSFT stock performance")
plt.plot(data.index, data['Close'])
plt.plot(data.index, data['SMA_20'])
plt.fill_between(data.index, data['Close'])
plt.show()
