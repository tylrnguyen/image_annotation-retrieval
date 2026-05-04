from app.event_generator import EventGenerator
from app.events import is_valid_event


def test_generator_creates_valid_image_submitted_event():
    generator = EventGenerator()
    event = generator.make_image_submitted_event()

    assert is_valid_event(event)
    assert event["topic"] == "image.submitted"
    assert "image_id" in event["payload"]


def test_generator_creates_malformed_event():
    generator = EventGenerator()
    event = generator.make_malformed_event()

    assert not is_valid_event(event)


def test_duplicate_event_has_same_event_id():
    generator = EventGenerator()
    event = generator.make_image_submitted_event()
    duplicate = generator.make_duplicate_event(event)

    assert duplicate["event_id"] == event["event_id"]