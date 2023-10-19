from keys import *
from  alpaca.trading import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus

trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)

get_orders_data = GetOrdersRequest(
    status=QueryOrderStatus.ALL,
    limit=100,
    nested=True
) # type: ignore

orders = trading_client.get_orders(get_orders_data)
print(orders)

# for properties, value in orders:
#     print(f'{properties} : {value}')