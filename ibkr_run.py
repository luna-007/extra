from ibapi.client import *
from ibapi.common import BarData, TickAttrib, TickerId
from ibapi.ticktype import TickType
from ibapi.wrapper import *
import datetime as dt
import pytz
import time

class IBapi(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)


    def nextValidId(self, orderId: int):

        # end_date = dt.datetime(2023, 1, 1, 15, 0, 0,0,pytz.timezone('UTC'))
        mycontract = Contract()
        mycontract.symbol = "EUR"
        mycontract.secType = "CASH"
        mycontract.exchange = "IDEALPRO"
        mycontract.currency = "USD"

        self.reqHistoricalData(orderId, mycontract, "20221010 15:00:00 US/Eastern", "1 D", "1 hour", "TRADES", 0, 1, 0, [])

    #     self.reqMarketDataType(4)
    #     self.reqMktData(orderId, mycontract, "", 0, 0, [])

    # def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
    #     print(f"Tick Price. reqId: {reqId}, ticktype: {TickTypeEnum.to_str(tickType)}, price: {price}, attribs: {attrib}")
    #     return super().tickPrice(reqId, tickType, price, attrib)
    
    # def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
    #     print(f"TickSize, reqId: {reqId}, ticktype: {TickTypeEnum.to_str(tickType)}, size: {size}")
    #     return super().tickSize(reqId, tickType, size)

    def historicalData(self, reqId: int, bar: BarData):
        print(f"Historical Data: {bar}")
        return super().historicalData(reqId, bar)
    
    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print("End of Historical Data")
        print(f'Start: {start}, End: {end}')
        return super().historicalDataEnd(reqId, start, end)




app = IBapi()
app.connect('127.0.0.1', 7497, 123)
app.run()
