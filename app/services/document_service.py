from datetime import datetime, timezone

from app.broker import Broker
from app.events import INFERENCE_COMPLETED, ANNOTATION_STORED, is_valid_event
from app.storage.mongo_client import MongoAnnotationStore


broker = Broker()
store = MongoAnnotationStore()


def handle_inference_completed(event):
    if not is_valid_event(event):
        print("Document Service: invalid event")
        return

    print("Document Service received:", event)

    payload = event.get("payload", {})
    image_id = payload.get("image_id")
    objects = payload.get("objects", [])
    model_version = payload.get("model_version", "unknown")

    if not image_id:
        print("Document Service: missing image_id")
        return

    result = store.store_annotation(
        image_id=image_id,
        objects=objects,
        model_version=model_version
    )

    print("Stored document in MongoDB Atlas:", result)

    new_event = {
        "event_id": f"evt_store_{image_id}",
        "topic": ANNOTATION_STORED,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": image_id,
            "status": "stored",
            "document_id": result["document_id"],
            "inserted": result["inserted"]
        }
    }

    broker.publish(ANNOTATION_STORED, new_event)
    print("Document Service published:", new_event)


def start():
    broker.subscribe(INFERENCE_COMPLETED, handle_inference_completed)
    print("Document Service is running and subscribed to inference.completed...")