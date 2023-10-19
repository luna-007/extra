from keys import *
import requests
import websocket, json

headers = {
    'Accept': 'text/event-stream',
}

params = {
    'token': SECRET_KEY,
    'symbols': 'spy',
}

response = requests.get('https://cloud-sse.iexapis.com/v1/news-stream', params=params, headers=headers)

print(response.text)

def on_open(ws):
    print("Opened")

def on_message(ws, message):
    print("Recieved a message")
    print(message)

socket = 'https://cloud-sse.iexapis.com/v1/news-stream'
ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message)
ws.run_forever()