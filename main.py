import json
import threading
import argparse
try:
    import websocket
except ImportError:
    import pip
    pip.main(["install", "websocket-client"])
    import websocket


def load_file(filepath):
    """Helper function to load file content."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    return content


def on_close(wsapp, close_status_code, close_msg):
    global close_flag
    close_flag = True
    print("WebSocket Closed", close_status_code, close_msg)


def on_open(wsapp):
    global close_flag
    close_flag = False
    print("WebSocket Connected")
    wsapp.send(json.dumps({"token": "anonymous"}))
    wsapp.send(json.dumps({"protocol": "custom-test:20190309"}))
    data = {
        "code": _CODE,
        "language": _LANGUAGE
    }
    wsapp.send(json.dumps(data))
    data = {
        "type": "text",
        "content": _INPUT
    }
    wsapp.send(json.dumps(data))


def on_message(wsapp, msg):
    msg = json.loads(msg)
    if msg.get("type") == "partial":
        i = msg
        print(f"{msg.get('name')} {msg.get('status')}")
        print(f"{i.get('detail')}")


def main(args):
    global _CODE, _LANGUAGE, _INPUT
    _CODE = load_file(args.code_file)
    _LANGUAGE = args.language
    _INPUT = "" if not args.input_file else load_file(args.input_file)

    ws_app = websocket.WebSocketApp(
        args.url,
        on_message=on_message,
        on_open=on_open,
        on_close=on_close
    )
    ws_thread = threading.Thread(target=ws_app.run_forever)
    ws_thread.start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LocalJudge: Judge your code remotely.")
    parser.add_argument("-c", "--code-file", type=str, required=True, help="Path to the code file (e.g., solution.cpp)")
    parser.add_argument("-i", "--input-file", type=str, default=False, help="Path to the input file (e.g., input.txt)")
    parser.add_argument("-l", "--language", type=str, choices=["C", "C++", "C++17"], default="C++17", help="Programming language to use")
    parser.add_argument("-u", "--url", type=str, default="wss://api.duck-ac.cn/", help="WebSocket server URL")
    
    args = parser.parse_args()
    main(args)
