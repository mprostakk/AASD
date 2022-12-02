import os
import time

from agent_test import DummyAgent


def main():
    xmpp_server_url = f"{os.environ['XMPP_SERVER_HOST']}@{os.environ['XMPP_SERVER_URL']}"
    xmpp_server_password = os.environ["XMPP_SERVER_PASSWORD"]
    dummy = DummyAgent(xmpp_server_url, xmpp_server_password)

    future = dummy.start()
    future.result()

    print("Wait until user interrupts with ctrl+C")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")

    dummy.stop()


if __name__ == "__main__":
    main()
