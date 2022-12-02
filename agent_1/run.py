import os
import time
import websocket

from agent_test import DummyAgent


def main():
    xmpp_server_url = f"{os.environ['XMPP_SERVER_HOST']}@{os.environ['XMPP_SERVER_URL']}"
    xmpp_server_password = os.environ["XMPP_SERVER_PASSWORD"]
    dummy = DummyAgent(xmpp_server_url, xmpp_server_password)

    future = dummy.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")

    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:9007")

    try:
        while True:
            time.sleep(1)
            ws.send("Hello, Server")

    except KeyboardInterrupt:
        print("Stopping...")

    dummy.stop()
    ws.close()


if __name__ == "__main__":
    main()
