from app.broker import Broker
from app.events import IMAGE_SUBMITTED, IMAGE_EVENTS_CHANNEL
from datetime import datetime, timezone

broker = Broker()

def submit_image():
    event = {
        "event_id": "evt_1",
        "topic": IMAGE_SUBMITTED,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": "img_123",
            "path": "test.jpg",
            "source": "cli"
        }
    }

    broker.publish(IMAGE_EVENTS_CHANNEL, event)
    print("Image submitted:", event)