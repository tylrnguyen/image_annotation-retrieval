from app.events import IMAGE_SUBMITTED, is_valid_event

def test_valid_event_schema():
    event = {
        "event_id": "evt_1",
        "topic": IMAGE_SUBMITTED,
        "timestamp": "2026-04-14T00:00:00Z",
        "payload": {"image_id": "img_1"}
    }

    assert is_valid_event(event)

def test_invalid_event_missing_event_id():
    event = {
        "topic": IMAGE_SUBMITTED,
        "timestamp": "2026-04-14T00:00:00Z",
        "payload": {"image_id": "img_1"}
    }

    assert not is_valid_event(event)