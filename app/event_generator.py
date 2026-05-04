from datetime import datetime, timezone
from uuid import uuid4
import time

from app.broker import Broker
from app.events import IMAGE_SUBMITTED

broker = Broker()

class EventGenerator:
    def make_image_submitted_event(self, image_path="images/test.jpg", source="generator"):
        image_id = f"img_{uuid4().hex[:8]}"

        return {
            "event_id": f"evt_{uuid4().hex[:8]}",
            "topic": IMAGE_SUBMITTED,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": {
                "image_id": image_id,
                "path": image_path,
                "source": source
            }
        }

    def publish_event(self, event):
        broker.publish(event["topic"], event)
        print("Event Generator published:", event)

    def publish_duplicate_event(self, event):
        broker.publish(event["topic"], event)
        broker.publish(event["topic"], event)
        print("Event Generator published duplicate event twice:", event)

    def make_malformed_event(self):
        return {
            "topic": IMAGE_SUBMITTED,
            "payload": {
                "path": "images/test.jpg"
            }
        }

    def publish_malformed_event(self):
        event = self.make_malformed_event()
        broker.publish(IMAGE_SUBMITTED, event)
        print("Event Generator published malformed event:", event)

    def publish_delayed_event(self, event, delay_seconds=2):
        time.sleep(delay_seconds)
        broker.publish(event["topic"], event)
        print("Event Generator published delayed event:", event)