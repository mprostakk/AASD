import os

import websocket
from functools import lru_cache


@lru_cache()
def get_ws_connection():
    ws = websocket.WebSocket()
    ws.connect(f"ws://{os.environ['WS_URL']}:{os.environ['WS_PORT']}")
    return ws
