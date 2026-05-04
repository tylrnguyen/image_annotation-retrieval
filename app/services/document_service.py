from datetime import datetime, timezone

from app.broker import Broker
from app.events import (
    INFERENCE_EVENTS_CHANNEL,
    ANNOTATION_EVENTS_CHANNEL,
    ANNOTATION_STORED,
)

broker = Broker()
DOCUMENT_DB = {}

def handle_inference_completed(event):
    print("Document Service received:", event)

    payload = event.get("payload", {})
    image_id = payload.get("image_id")

    if not image_id:
        print("Document Service: invalid event, missing image_id")
        return

    if image_id in DOCUMENT_DB:
        print(f"Document for {image_id} already exists. Skipping duplicate.")
        return

    document = {
        "image_id": image_id,
        "objects": payload.get("objects", []),
        "model_version": payload.get("model_version", "unknown"),
        "status": "stored"
    }

    DOCUMENT_DB[image_id] = document
    print("Stored document:", document)

    new_event = {
        "event_id": f"evt_store_{image_id}",
        "topic": ANNOTATION_STORED,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": image_id,
            "status": "stored",
            "document_id": f"doc_{image_id}"
        }
    }

    broker.publish(ANNOTATION_EVENTS_CHANNEL, new_event)
    print("Document Service published:", new_event)

def start():
    broker.subscribe(INFERENCE_EVENTS_CHANNEL, handle_inference_completed)
    print("Document Service is running and subscribed to inference_events...")