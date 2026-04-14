from app.broker import Broker
from datetime import datetime, timezone

broker = Broker()

def handle_image_submitted(event):
    print("Inference received:", event)

    payload = event.get("payload", {})
    image_id = payload.get("image_id")

    if not image_id:
        print("Inference Service: invalid event, missing image_id")
        return

    new_event = {
        "event_id": "evt_2",
        "topic": "inference.completed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": image_id,
            "objects": [
                {
                    "label": "car",
                    "conf": 0.9
                }
            ],
            "model_version": "sim_v1"
        }
    }

    broker.publish("inference_events", new_event)
    print("Inference published:", new_event)

def start():
    broker.subscribe("image_events", handle_image_submitted)
    print("Inference Service is running and subscribed to image_events...")