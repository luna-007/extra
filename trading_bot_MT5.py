#Importing the necessary libararies
import MetaTrader5 as mt5
import pandas as pd
import time
from datetime import datetime as dt
from colorama import Back, Fore

#setting variables which will be used 
symbol = 'EURUSD'
volume = float(10)
deviation= 1
short_filter = '13_day_ema'
# long_filter = '39_day_ema'
filter_by = 13
sec_filter = 39
sleep = 30


"""How to get the final position of trades whose stoploss got hit"""
""""""

#Establishing connection with the Terminal
if not mt5.initialize():
    print("Not able to initialize")
    quit()

"""
Functions
"""

def order_status(order):
    execution_status=True
    while execution_status:
        if order[0] != 10009:
            print(Fore.YELLOW + "Trying with increased deviation for new order: ")
            order_type = order[10][10]
            if order_type==1:
                order_ = sell_order(symbol, deviation=deviation + 10)
                print(Fore.BLUE+ "Order Condition For Sell: ", order_[7])
                order_status(order_) 
                execution_status = False
                return order_
            elif order_type ==0:
                order_ = buy_order(symbol, deviation=deviation + 10)
                print(Fore.BLUE + "Order Condition For Buy: ", order_[7])
                order_status(order_)
                execution_status = False
                return order_
        if order[0] == 10009:
            print("Request Executed for initiating a new position: ", order[7])
            execution_status = False
            return order
        else:
            print("Some Other Execution Error")
            print("Publishing the Order below \n")
            print(order[7])
            SystemExit(0)

"""Change the below function to fit for both buy and sell order executions
instead of just closing position scenarios"""

def order_status_close(order):
    execution_status=True
    while execution_status:
        if order[0] != 10009:
            ticket, volume, entry = get_ticket_data()
            print(Fore.YELLOW + "Close: Trying with increased deviation for new order: ")
            order_type = order[10][10]
            if order_type==1:
                order_ = close_position(symbol, ticket, volume, deviation + 10)
                print(Fore.BLUE+ "Order Condition For Sell: ", order_[7])
                order_status_close(order_) 
                execution_status = False
                return order_
            elif order_type ==0:
                order_ = buy_order(symbol, deviation + 10)
                print(Fore.BLUE + "Order Condition For Buy: ", order_[7])
                order_status_close(order_)
                execution_status = False
                return order_
        if order[0] == 10009:
            print("Request Executed for closing position: ", order[7])
            execution_status = False
            return order
        else:
            print("Some Other Execution Error")
            print("Publishing the Order below \n")
            print(order[7])
            SystemExit(0)
        
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
    except Exception as e:
        positions = -1
        long_pos = False
        short_pos = False
        return long_pos, short_pos

    return long_pos, short_pos

#Getting the Order Number and the position size
def get_ticket_data():
    positions = mt5.positions_get()
    if len(positions) != 0:
        return positions[0][0], positions[0][9], positions[0][10]
    else: 
        print(Fore.YELLOW + "No open Positions to get ticket from ") 
        return 0, 0, 0
    

#Getting historical data and generating indicators etc.
def train_data():

    # To Generate Signals from a different timeframe and implement it on a different one

    # signal = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 100)
    # signal_frame = pd.DataFrame(signal)
    # signal_frame['time'] = pd.to_datetime(signal_frame['time'], unit='s')
    # signal_frame.drop(['spread', 'real_volume'], axis=1, inplace=True)
    # signal_frame['ema'] = rates_frame['close'].rolling(filter_by).mean()
    # signal_frame['sma'] = rates_frame['close'].rolling(sec-filter).mean()
    # print(signal_frame.iloc[-1][['sma', 'ema']])


    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 600)
    rates_frame = pd.DataFrame(rates)
    rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
    rates_frame.drop(['spread', 'real_volume'], axis=1, inplace=True)
    rates_frame[short_filter] = rates_frame['close'].ewm(span=filter_by).mean()
    # rates_frame[long_filter] = rates_frame['close'].ewm(span=sec_filter).mean()
    print(Fore.BLUE + f'{rates_frame.iloc[-1][[short_filter, "close"]]}')
    return rates_frame

def get_final_pos(order):

    if len(order) != 0:

        ticket = order[2]
        pos_details = mt5.positions_get(ticket=ticket)
        profit = pos_details[0][15] 
        order_type = pos_details[0][5]
        if order_type == 1:
            print(dt.now(), Fore.RED + "The Current Short Position is: ", profit)
        elif order_type == 0:
            print(dt.now(), Fore.GREEN + "The Current Long Position is: ", profit)
        else:
            print(Fore.RED + "Some Error In Calculating current Position")

        return profit

    elif len(order) == 0:
        
        open_pos = mt5.positions_get(symbol=symbol)
        try:
            profit = open_pos[0][15]
            pos_type = open_pos[0][5]
            if pos_type == 0:
                print(Fore.GREEN + "EXISTING:  The Current Long Position is: ", profit)
            elif pos_type == 1:
                print(Fore.RED + "EXISTING:  The Current Short Position is: ", profit)
            return profit
        except Exception as e:
            print(Fore.YELLOW + "No Open Positions")
            return 0
            
def close_bal(volume, entry_price, price, type):

    if type:
        net_pos = (price - entry_price) * volume * 100000
        print(Fore.YELLOW + "Last Closed Long Position: ", round(net_pos, 2))
    else:
        net_pos = (entry_price - price) * volume * 100000
        print(Fore.YELLOW + "Last closed Short Position: ", round(net_pos, 2))

#Function for sending buy orders
def buy_order(symbol, deviation=5):

    price = mt5.symbol_info_tick(symbol).ask
    buy_price = float(price)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": float(buy_price - (buy_price * 0.00030)),
        "tp": float(buy_price + (buy_price * 0.00045)),
        "deviation" : deviation,
        "comment": "Buy Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    order = order_status(mt5.order_send(request))
    return order

#Function for sending sell orders
def sell_order(symbol, deviation=5):

    price = mt5.symbol_info_tick(symbol).bid
    sell_price = float(price)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": volume,
        "type": mt5.ORDER_TYPE_SELL,
        "price": price,
        "sl": float(sell_price + (sell_price * 0.00030)),
        "tp": float(sell_price - (sell_price * 0.00045)),
        "deviation": deviation,
        "comment": "Sell Order",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN
    }

    order = order_status(mt5.order_send(request))
    return order

#Function to close any open positions when the trend changes
def close_position(enter, ticket, volume, entry_price, deviation=5):

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
            "type_filling": mt5.ORDER_FILLING_RETURN,
            "position": ticket
        }

        buy_ = order_status_close(mt5.order_send(request))
        close_bal(volume, entry_price, price, True)
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
            "type_filling": mt5.ORDER_FILLING_RETURN,
            "position": ticket
        }

        sell_ = order_status_close(mt5.order_send(request))
        close_bal(volume, entry_price, price, False)
        return sell_
    

#Execution Function which sends orders based on the signals generated
def main(short_filter):

    pos = ()
    while True:
        
        long_pos, short_pos = position_type()
        ticket, volume, entry_price = get_ticket_data()
        price_data = train_data()

        #Long Position Trigger
        if price_data[short_filter].iloc[-1] < price_data['close'].iloc[-1]:
            # print('Crossover: Long Position should Initiate')
            print(Fore.GREEN + "Crossover: 13 EMA is higher is than close")
            print(Fore.GREEN + "Go LONG")
            if long_pos == False and short_pos == False:
                pos = buy_order(symbol)
                long_pos = True
                print(dt.now(),Fore.GREEN + ' No Existing Short Position, Initiated a long')
            elif long_pos == False and short_pos == True:
                pos = close_position(symbol, ticket, volume, entry_price) #Entry Price is added for profit/loss calculation
                pos = buy_order(symbol)
                long_pos = True
                short_pos = False
                print(dt.now(),Fore.GREEN + ' Short Position Exited and Long Position Initiated')
            elif long_pos == True:
                print(dt.now(),Fore.GREEN + " Long: Already with the trend")

        #Short Position Trigger
        elif price_data['close'].iloc[-1] < price_data[short_filter].iloc[-1]:
            # print("Crossover: Short Position should Initiate")
            print(Fore.RED + "Crossover: 13 EMA is lower is than close")
            print(Fore.RED + "Go SHORT")
            if short_pos == False and long_pos == False:
                pos = sell_order(symbol)
                print(dt.now(), Fore.RED + ' No Existing Long Position, Initiated a Short')
                short_pos = True
                long_pos = False
            elif short_pos == False and long_pos == True:
                pos = close_position(symbol, ticket, volume, entry_price)
                pos = sell_order(symbol)
                short_pos = True
                print(dt.now(), Fore.RED + " Long position Exited and Short Position Initiated")
            elif short_pos == True:
                print(dt.now(), Fore.RED + " Short: Already with the trend")
        
        get_final_pos(pos)
      
        time.sleep(sleep) #Keeps refreshing to update data and take actions

#Execution
main(short_filter)

#Shutdown
mt5.shutdown()