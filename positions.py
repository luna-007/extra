import MetaTrader5 as mt5
import pandas as pd



if not mt5.initialize():
    print("Not Initialized")
    quit()

# print(mt5.account_info())

def get_ticket():
    data = mt5.positions_get()
    # print("Position is: ",data[0][15])
    return data


# ticket = 50726333578
# print(mt5.orders_get(ticket=ticket))
data = get_ticket()
for pos in data:
    print(pos.ticket)
# print("Type: ",data[0][5])
# print("Price: ",data[0][15])
# print(mt5.positions_get())

# rates = mt5.copy_rates_from_pos('EURUSD', mt5.TIMEFRAME_M5, 0, 100)
# data = pd.DataFrame(rates)
# print(data)

# get_ticket()

# def get_price():
#     data = mt5.copy_rates_from_pos('EURUSD', mt5.TIMEFRAME_M1, 0, 60)
#     data = pd.DataFrame(data)
#     print(data)
# data = get_ticket()
# print(data[0][17] == 'Sell Order')
# print(len(data))
# print(data[0][9])

symbol = 'EURUSD'
volume = float(1)

price = mt5.symbol_info_tick(symbol).ask
request = {
     "action": mt5.TRADE_ACTION_DEAL,
     "symbol": symbol,
     "volume": volume,
     "type": mt5.ORDER_TYPE_SELL,
     "price": price,
     "deviation" : 1,
     "comment": "Closing Long",
     "type_time": mt5.ORDER_TIME_GTC,
     "type_filling": mt5.ORDER_FILLING_RETURN
     }

sec_price = mt5.symbol_info_tick(symbol).bid
sec_request = {
     "action": mt5.TRADE_ACTION_DEAL,
     "symbol": symbol,
     "volume": volume,
     "type": mt5.ORDER_TYPE_SELL,
     "price": sec_price,
     "deviation" : 20,
     "comment": "Closing Long",
     "type_time": mt5.ORDER_TIME_GTC,
     "type_filling": mt5.ORDER_FILLING_RETURN
     }

# buy_ = mt5.order_send(sec_request)
# order_status(buy_)
# print(buy_)
# print("Type: ", buy_[0])

# def order_check(order):
#     status = False
#     i = 0
#     while (i < 3):
#         i += 1
#         if order[0] != 10009:
#             order_ = mt5.order_send(sec_request)
#             print("Second One Hit", print(order_[0]))
#             order_check(order_)
#             i = 5
#             if i < 3:
#                 print("This is just a checkpoint")
#             if status:
#                 status=True
#                 print("Second Checkpoint")
#         if order[0] == 10009:
#             print("Placed")
#             i = 5
#             status = True
#         else:
#             break

# order_check(buy_)


# print(mt5.orders_get())



"""

OrderSendResult(retcode=10004, 
deal=0, 
order=0, volume=0.0, price=0.0, 
bid=1.05038, ask=1.05042, comment='Requote', 
request_id=467897669, retcode_external=0, 
request=TradeRequest(action=1, magic=0, order=0, 
symbol='EURUSD', volume=1.0, price=1.05035, stoplimit=0.0, 
sl=0.0, tp=0.0, deviation=2, type=1, type_filling=2, 
type_time=0, expiration=0, comment='Closing Long', position=0, position_by=0))

"""




# price = mt5.symbol_info_tick(symbol).bid
# buy_price = price

# request = {
#     "action": mt5.TRADE_ACTION_DEAL,
#     "symbol": symbol,
#     "volume": volume,
#     "type": mt5.ORDER_TYPE_SELL,
#     "price": price,
#     "sl": float(buy_price + (buy_price * 0.0002)),
#     "tp": float(buy_price - (buy_price * 0.0002)),
#     "deviation" : 50,
#     "comment": "Sell Order",
#     "type_time": mt5.ORDER_TIME_GTC,
#     "type_filling": mt5.ORDER_FILLING_RETURN
#     }

# order = mt5.order_send(request)
# print(order)
# print("TIcket: ", order[2])
# deal_ticket = order[1]

# deal = mt5.history_deals_get(ticket = 50711014292)
# deal = mt5.history_deals_get(position= 50719093057)
# sell_deal = mt5.history_deals_get(ticket = 50711059233)
# print(deal[0][10])
# print(deal)
# print("===============================")
# print(sell_deal[0][4])
# print(sell_deal)
# print(order[1])


# def get_ticket():
#     positions = mt5.orders_get()
#     # print(positions)
#     print(positions[0:4])

# print(mt5.symbol_info_tick('EURUSD').ask)
# print(mt5.account_info())


# ticket = get_ticket()
# print(ticket)