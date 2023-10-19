from alpaca.trading.requests import OrderRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from keys import *


client = TradingClient(API_KEY, SECRET_KEY)

def buy_order(symbol, qty):

    buy_order = OrderRequest(
        symbol=symbol,
        qty=qty,
        side = OrderSide.BUY,
        time_in_force=TimeInForce.GTC,
        type= OrderType.MARKET
        )

    return client.submit_order(buy_order)

def sell_order(symbol, qty):

    sell_order = OrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.SELL,
        time_in_force=TimeInForce.GTC,
        type= OrderType.MARKET
    )

    return client.submit_order(sell_order)

