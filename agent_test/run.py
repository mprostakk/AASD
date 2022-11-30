from agent_test import DummyAgent
import os
from dotenv import load_dotenv
import time
load_dotenv()

dummy = DummyAgent(os.environ['SERVER_URI'], os.environ['SERVER_PASSWORD'])
future = dummy.start()
future.result()

print("Wait until user interrupts with ctrl+C")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")
dummy.stop()