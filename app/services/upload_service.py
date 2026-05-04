from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone

from app.broker import Broker
from app.events import IMAGE_SUBMITTED, IMAGE_EVENTS_CHANNEL

broker = Broker()

def submit_image(image_path: str, source: str = "cli"):
    path = Path(image_path)

    if not path.exists():
        print(f"Upload Service: file does not exist -> {image_path}")
        return None

    event = {
        "event_id": f"evt_{uuid4().hex[:8]}",
        "topic": IMAGE_SUBMITTED,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": f"img_{uuid4().hex[:8]}",
            "path": str(path),
            "source": source
        }
    }

    broker.publish(IMAGE_EVENTS_CHANNEL, event)
    print("Upload Service published:", event)
    return event