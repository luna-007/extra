from keys import *
from alpaca.trading import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

api_key = API_KEY
secret_key = SECRET_KEY

trading_client = TradingClient(api_key, secret_key, paper=True)


def place_order(symbol, qty, side):
    """
    To properly execute the trade, provide the symbol in string format or list of strings and must use side = 'b' for buying and 's' for selling
    """
    
    if side == 'b':
        marketorderdata = MarketOrderRequest(
            symbol = symbol,
            qty = qty,
            side = OrderSide.BUY,
            time_in_force = TimeInForce.GTC
        )
    elif side == 's':
        marketorderdata = MarketOrderRequest(
            symbol = symbol,
            qty = qty,
            side = OrderSide.SELL,
            time_in_force = TimeInForce.GTC
        )
    else:
        print("Please Check you order parameters")

    return marketorderdata 
    
marketorder = trading_client.submit_order(place_order('SPY', 1, 'b'))

for properties, value in marketorder:
    print(f'{properties}: {value}')