import websocket
import json
import requests
import pandas as pd

symbol = 'ethusdt'

# url = f'wss://stream.binance.com:9443/ws/{symbol}@trade'
url = 'wss://stream.binance.com:9443/ws'
# url = f'wss://testnet.binance.vision/ws-api/v3{symbol}@trade'


def on_message(ws, message):

    data = json.loads(message)
    df = pd.Series(data)
    df = pd.DataFrame(data, index=['i',])
    print(df)

def on_open(ws):
    print("Connection Successful")
    
    requests = {
        "method": "SUBSCRIBE",
        "params": ["ethusdt@trade"],
        "id": 1
    }

    ws.send(json.dumps(requests))

def on_close(ws):
    print('Close')

ws = websocket.WebSocketApp(url, on_open=on_open,on_close=on_close,on_message=on_message)
ws.run_forever()