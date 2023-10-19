#Importing the necessary libararies
import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime as dt

#setting variables which will be used 
symbol = 'BTCUSD'
volume = float(0.5)
filter = 'sma'
filter_by = 30

#Establishing connection with the Terminal
if not mt5.initialize():
    print("Not able to initialize")
    quit()

print(mt5.account_info())

#Get all the open positions
positions = mt5.positions_get()

"""
Functions
"""

def order_status(order):
    if len(order) != 0:
        if order[7] == 'Requote':
            try:
                print("Trying with increased deviation")
                ticket, volume = get_ticket_data()
                close_position(symbol, ticket, volume, 10)
            except Exception as e:
                print("Executed Try and Error")
                print("Reason For Error: ", order[7])
                raise SystemExit(0)
        elif order[7] == 'Request executed':
            print("Check Performed and No Errors Found")
    else:
        print("Checking Execution: ", order)


#Function to figure out if the positions or short or long positions
def position_type():
    positions = mt5.positions_get()
    try:
        positions = positions[0][5]
        if positions == 1:
            short_pos = True
            long_pos = False
        elif positions == 0:
            long_pos = True
            short_pos = False
        else:
            return False, False
    except:
        positions = -1
        long_pos = False
        short_pos = False
        return long_pos, short_pos
    
    # print("Short Position: ", short_pos)
    # print("Long Position: ", long_pos)
    return long_pos, short_pos

#Getting the Order Number and the position size
def get_ticket_data():
    positions = mt5.positions_get()
    if len(positions) != 0:
        return positions[0][0], positions[0][9]
    else: 
        print("No open Positions to get ticket from ") 
        return 0, 0
    

#Getting historical data and generating indicators etc.
def train_data():

    # signal = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
    # signal_frame = pd.DataFrame(signal)
    # signal_frame['time'] = pd.to_datetime(signal_frame['time'], unit='s')
    # signal_frame.drop(['spread', 'real_volume'], axis=1, inplace=True)
    # signal_frame['ema'] = rates_frame['close'].ewm(span=filter_by).mean()
    # signal_frame['sma'] = rates_frame['close'].rolling(filter_by).mean()
    # print(signal_frame.iloc[-1][['sma', 'ema']])


    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame.drop(['spread', 'real_volume'], axis=1, inplace=True)
    rates_frame['sma'] = rates_frame['close'].rolling(filter_by).mean()
    rates_frame['ema'] = rates_frame['close'].ewm(filter_by).mean()
    print(rates_frame.iloc[-1][['sma' ,'ema', 'close']])
    return rates_frame

#Function for sending buy orders
def buy_order(symbol):

    price = mt5.symbol_info_tick(symbol).ask
    buy_price = price

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": float(buy_price - (buy_price * 0.005)),
        "tp": float(buy_price + (buy_price * 0.002)),
        "deviation" : 5,
        "comment": "Buy Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    order = mt5.order_send(request)
    order_status(order)
    # print(order)
    print('Checking if go Long Order was sent: ', order[7])
    return order

#Function for sending sell orders
def sell_order(symbol):

    price = mt5.symbol_info_tick(symbol).bid
    sell_price = price
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": float(sell_price + (sell_price * 0.005)),
        "tp": float(sell_price - (sell_price * 0.002)),
        "deviation": 5,
        "comment": "Sell Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC
    }

    order = mt5.order_send(request)
    # print(order)
    order_status(order)
    print('Checking if go Short Order was sent: ', order[7])
    return order

#Function to close any open positions when the trend changes
def close_position(enter, ticket, volume, deviation=5):

    long_pos, short_pos = position_type()

    if (long_pos == True):

        price = mt5.symbol_info_tick(enter).bid
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": enter,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation" : deviation,
            "comment": "Closing Long",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            "position": ticket
        }

        buy_ = mt5.order_send(request)
        order_status(buy_)
        # print(buy_)
        print("Checking If Long Close Order Executed: ", buy_[7])
        return buy_
    
    elif (short_pos == True):

        price = mt5.symbol_info_tick(enter).ask
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": enter,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "deviation" : deviation,
            "comment": "Closing Short",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
            "position": ticket
        }

        sell_ = mt5.order_send(request)
        order_status(sell_)
        # print(sell_)
        print("Checking If Short close Order Executed: ", sell_[7])
        return sell_

#Execution Function which sends orders based on the signals generated
def trigger(filter):


    while True:
        
        long_pos, short_pos = position_type()
        ticket, volume = get_ticket_data()
        price_data = train_data()

        #Long Position Trigger
        if price_data[filter].iloc[-1] < price_data['close'].iloc[-1]:
            print('Crossover: Long Position should Initiate')
            if long_pos == False and short_pos == True:
                close_position(symbol, ticket, volume)
                buy_order(symbol)
                long_pos = True
                short_pos = False
                print(dt.now(),' Short Position Exited and Long Position Initiated')
            elif long_pos == False and short_pos == False:
                buy_order(symbol)
                long_pos = True
                print(dt.now(),' No Existing Short Position, Initiated a long')
            elif short_pos == True:
                close_position(symbol, ticket, volume)
                short_pos = False
                print(dt.now()," Open Short position closed as trend changed")
            elif long_pos == True:
                print(dt.now()," Long: Already with the trend")

        #Short Position Trigger
        elif price_data[filter].iloc[-1] > price_data['close'].iloc[-1]:
            print("Crossover: Short Position should Initiate")
            if short_pos == False and long_pos == True:
                close_position(symbol, ticket, volume)
                sell_order(symbol)
                print(dt.now(), " Long position Exited and Short Position Initiated")
                short_pos = True
                long_pos = False
            elif short_pos == False and long_pos == False:
                sell_order(symbol)
                short_pos = True
                print(dt.now(), ' No Existing Long Position, Initiated a Short')
            elif long_pos == True:
                close_position(symbol, ticket, volume)
                long_pos = False
                print(dt.now(), " Open Long Position Closed as trend changed")
            elif short_pos == True:
                print(dt.now(), " Short: Already with the trend")

        time.sleep(60) #Keeps refreshing to update data and take actions

#Execution
trigger(filter)

#Shutdown
mt5.shutdown()