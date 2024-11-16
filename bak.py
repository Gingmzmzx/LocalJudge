import json
import threading
try:
    import websocket
except ImportError:
    import pip
    pip.main("install websocket-client".split())
    import websocket


with open("solution.cpp", "r", encoding="utf-8") as f:
    _CODE = f.read()
_LANGUAGE = "C++17"  # C, C++, C++17
with open("input.txt", "r", encoding="utf-8") as f:
    _INPUT = f.read()


def on_close(wsapp, close_status_code, close_msg):
    global close_flag
    close_flag = True
    print("WebSocket Closed", close_status_code, close_msg)

def on_open(wsapp):
    global close_flag
    close_flag = False
    print("WebSocket Connected")
    ws_app.send('{"token":"anonymous"}')
    ws_app.send('{"protocol":"custom-test:20190309"}')
    data = {
        "code": _CODE,
        "language": _LANGUAGE
    }
    ws_app.send(json.dumps(data))
    data = {
        "type": "text",
        "content": _INPUT
    }
    ws_app.send(json.dumps(data))

def on_message(wsapp, msg):
    msg = json.loads(msg)
    if msg.get("type") == "partial":
        i = msg
        print(f"{msg.get('name')} {msg.get('status')}")
        print(f"{i.get('detail')}")

ws_app = websocket.WebSocketApp("wss://api.duck-ac.cn/",
                            on_message=on_message,
                            on_open=on_open,
                            on_close=on_close)
ws_thread = threading.Thread(target=ws_app.run_forever)
ws_thread.start()
