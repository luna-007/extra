from keys import *
from alpaca.trading import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

end_point = ENDPOINT
api_key = API_KEY
secret_key = SECRET_KEY

api = alpacaapi