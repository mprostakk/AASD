from base_agent import AgentBaseBehaviour
from typing import Union
import json
import random
import os
from spade.message import Message

async def send(
    behaviour: AgentBaseBehaviour, 
    receivers_group: str,
    receivers_prefix: str,
    message_type: str,
    message_payload: dict
) -> None:
    receiver_count = int(os.environ.get("AGENT_"+receivers_group+"_NUMBER", 0))
    receiver_idx = random.randint(1, receiver_count)
    to = receivers_prefix + str(receiver_idx) + "@localhost"
    print("sending:", message_type, "  to:", to)

    msg_body = { 'type': message_type, 'payload': message_payload }
    raw_msg_body = json.dumps(msg_body)
    msg = Message(to=to)  # Instantiate the message
    msg.body = raw_msg_body  # Set the message content
    await behaviour.send(msg)

async def receive(behaviour: AgentBaseBehaviour, message_type: str, timeout: float) -> Union[dict, None]:
    msg = await behaviour.receive(timeout=timeout)

    if not msg: return
    if not msg.body: return

    msg_body = json.loads(msg.body)
    if msg_body['type'] != message_type: return

    print("receiving:", msg_body['type'])
    return msg_body