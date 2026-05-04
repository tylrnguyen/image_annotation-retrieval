from datetime import datetime, timezone

from app.broker import Broker
from app.events import ANNOTATION_STORED, EMBEDDING_CREATED, is_valid_event
from app.simulation.image_processing import simulate_embedding


broker = Broker()


def handle_annotation_stored(event):
    if not is_valid_event(event):
        print("Embedding Service: invalid event")
        return

    print("Embedding Service received:", event)

    payload = event.get("payload", {})
    image_id = payload.get("image_id")

    if not image_id:
        print("Embedding Service: missing image_id")
        return

    embedding = simulate_embedding(image_id, dimension=128)

    new_event = {
        "event_id": f"evt_embed_{image_id}",
        "topic": EMBEDDING_CREATED,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": image_id,
            "embedding": embedding,
            "dimension": 128,
            "embedding_model": "sim_embed_v1"
        }
    }

    broker.publish(EMBEDDING_CREATED, new_event)

    print(
        "Embedding Service published:",
        {
            "event_id": new_event["event_id"],
            "topic": new_event["topic"],
            "payload": {
                "image_id": image_id,
                "dimension": 128,
                "embedding_model": "sim_embed_v1"
            }
        }
    )


def start():
    broker.subscribe(ANNOTATION_STORED, handle_annotation_stored)
    print("Embedding Service is running and subscribed to annotation.stored...")