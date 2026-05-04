import time

from app.broker import Broker
from app.events import IMAGE_SUBMITTED


def test_redis_pubsub_receives_message():
    broker = Broker()
    received = []

    def handler(event):
        received.append(event)

    pubsub = broker.subscribe(IMAGE_SUBMITTED, handler)

    time.sleep(0.5)

    event = {
        "event_id": "evt_test",
        "topic": IMAGE_SUBMITTED,
        "timestamp": "2026-05-04T00:00:00Z",
        "payload": {
            "image_id": "img_test"
        }
    }

    broker.publish(IMAGE_SUBMITTED, event)

    time.sleep(0.5)

    assert len(received) == 1
    assert received[0]["topic"] == IMAGE_SUBMITTED
    assert received[0]["payload"]["image_id"] == "img_test"

    pubsub.close()