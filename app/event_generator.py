from datetime import datetime, timezone
from uuid import uuid4
import time

from app.events import IMAGE_SUBMITTED


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

    def make_duplicate_event(self, event):
        return event.copy()

    def make_malformed_event(self):
        return {
            "topic": IMAGE_SUBMITTED,
            "payload": {
                "path": "images/test.jpg"
            }
        }

    def make_delayed_event(self, event, delay_seconds=2):
        time.sleep(delay_seconds)
        return event