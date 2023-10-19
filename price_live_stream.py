import websocket, json
from keys import *
import asyncio


data = None

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "auth",
        "key": API_KEY,
        "secret": SECRET_KEY
    }

    ws.send(json.dumps(auth_data))

    
    channel_data = {
        "action": "subscribe",
        "quotes": ["AAPL"]
        }

    ws.send(json.dumps(channel_data))


def on_message(ws, message):
    global data
    print("received a message")
    data = json.loads(message)
    print("Price: ", data[0]['p'])
    print("Time: ", data[0]['t'])
    


socket = "wss://stream.data.alpaca.markets/v2/iex"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()