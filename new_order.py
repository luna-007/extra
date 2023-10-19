from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import *

import threading
import time

class IBapi(EWrapper, EClient):
    
    def __init__(self):
        EClient.__init__(self, self)
        
    def nextValidId(self, orderId: int):
        super().nextValidId(orderId)
        self.nextorderId = orderId
        print("The next valid orderId is: ", self.nextorderId)
        

def run_loop():
    app.run()
     
app = IBapi()
app.connect('127.0.0.1', 7497, 1)

app.nextorderId = None  # type: ignore

api_thread = threading.Thread(target=run_loop, daemon=True)
api_thread.start()

while True:
    if isinstance(app.nextorderId, int):
        print('connected')
        break
    else:
        print('waiting for connection')
        time.sleep(1)
        
def stock_contract(symbol, secType = 'STK', exchange = 'SMART', currency = 'USD'):  
    contract = Contract()
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    contract.symbol = symbol
    return contract

contract = stock_contract('AAPL')

def stock_order(action, totalQuantity, orderType, lmtPrice):
    order = Order()
    order.action = action
    order.totalQuantity = totalQuantity  
    order.orderType = orderType
    order.lmtPrice = lmtPrice  
    return order
    
order = stock_order('BUY', 100, 'LMT', 145.90)
    
# order = stock_order('BUY', 10, 'LMT', 145.90)

app.placeOrder(app.nextorderId, contract, order) 

# time.sleep(3)

# print('Cancelling Order')
# app.cancelOrder(app.nextorderId, '')

time.sleep(3)
app.disconnect()