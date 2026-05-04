from app.broker import Broker
from app.events import IMAGE_SUBMITTED, IMAGE_EVENTS_CHANNEL
import time

broker = Broker()

def handle_event(event):
    print(f"Received event: {event}")

# subscribe first
broker.subscribe(IMAGE_EVENTS_CHANNEL, handle_event)

time.sleep(1)  # give some time for the subscription to be set up

# publish an event
event_data = {
    "event_id": "evt_1",
    "topic": IMAGE_SUBMITTED,
    "payload": {
        "image_id": "img_123"
    }
}

broker.publish(IMAGE_EVENTS_CHANNEL, event_data)

time.sleep(2)  # wait to ensure the event is received before the script exits