from datetime import datetime, timezone

from app.broker import Broker
from app.events import IMAGE_SUBMITTED, INFERENCE_COMPLETED, is_valid_event

from app.simulation.image_processing import simulate_object_detection

broker = Broker()

def handle_image_submitted(event):
    print("Inference received:", event)
    payload = event.get("payload", {})
    image_id = payload.get("image_id")
    image_path = payload.get("path")

    if not image_id:
        print("Inference Service: invalid event, missing image_id")
        return

    objects = simulate_object_detection(image_id, image_path)

    new_event = {
        "event_id": f"evt_infer_{image_id}",
        "topic": INFERENCE_COMPLETED,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "image_id": image_id,
            "path": image_path,
            "objects": objects,
            "model_version": "sim_v1"
        }
    }

    broker.publish(INFERENCE_COMPLETED, new_event)
    print("Inference published:", new_event)

def start():
    broker.subscribe(IMAGE_SUBMITTED, handle_image_submitted)
    print("Inference Service is running and subscribed to image.submitted...")