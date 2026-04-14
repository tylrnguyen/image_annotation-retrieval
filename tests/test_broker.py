from app.broker import Broker
import time

broker = Broker()

def handle_event(event):
    print(f"Received event: {event}")

# subscribe first
broker.subscribe('test_channel', handle_event)

time.sleep(1)  # give some time for the subscription to be set up

# publish an event
event_data = {
    "event_id": "evt_1",
    "topic": "image_submitted",
    "payload": {
        "image_id": "img_123"
        }
    }

broker.publish('test_channel', event_data)

time.sleep(2)  # wait to ensure the event is received before the script exits