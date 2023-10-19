from alpaca.trading.client import TradingClient
from alpaca.data.models.trades import Trade
from order import *
from keys import *

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# print(trading_client.get_account())

# order_details = buy_order('AAPL', 5)
# print(order_details)

print(trading_client.get_orders())