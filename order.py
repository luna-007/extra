from ib_insync import *
import time
import pandas as pd
from dataclasses import asdict
import tabloo

ib = IB()
ib.connect('127.0.0.1', 7497, 3)

stock = Stock('AAPL', 'SMART','USD')

order = LimitOrder('BUY', 5, 75.13)

# trade = ib.placeOrder(stock, order)
# ids = order.orderId
portfolio = ib.portfolio()
# print(portfolio)
positions = []

counter = 0

for i in portfolio[0]:
    # print (type(i))
    positions.append(i)
    
# print(positions[0])

# for i in positions[0]:
    # print(i)
    
value = util.df(portfolio)
# print(type(positions[0]))
# print(value)

# data = pd.DataFrame(positions, columns=['one', 'two', 'three', 'four', 'five', 'six', 'seven'])
data = asdict(positions[0])

# new_data = util.df(data)
new_frame = pd.DataFrame([data])
# print(new_frame)

frames = [new_frame, value]
result = pd.concat(frames, axis=1)
result.drop(['contract'],axis=1, inplace=True)
# print(result)
tabloo.show(result)
#     for y in range(1):
        
    
    # positions.append(i)

# data = util.df(positions)
# print(data)

# new_data = util.df(positions[0])
# for i in positions[0]:
#     print(i[0])
# print(positions)
# news = ib.reqNewsBulletins(True)

# time.sleep(5)
# print(news)
# dataframe = pd.DataFrame(portfolio[1], columns=['one', 'two', 'three', 'four', 'five', 'six', 'seven'])

# print(type(portfolio[0]))