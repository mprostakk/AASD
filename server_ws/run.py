import logging
from websocket_server import WebsocketServer


def new_client(client, server):
    pass


def client_receive(client, server, msg):
    server.send_message_to_all(msg)


server = WebsocketServer(host="0.0.0.0", port=9007, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.set_fn_message_received(client_receive)
server.run_forever()
