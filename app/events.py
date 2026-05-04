IMAGE_SUBMITTED = "image.submitted"
INFERENCE_COMPLETED = "inference.completed"
ANNOTATION_STORED = "annotation.stored"
EMBEDDING_CREATED = "embedding.created"

# Channels for pub/sub
IMAGE_EVENTS_CHANNEL = "image_events"
INFERENCE_EVENTS_CHANNEL = "inference_events"
ANNOTATION_EVENTS_CHANNEL = "annotation_events"

REQUIRED_EVENT_FIELDS = ["event_id", "topic", "timestamp", "payload"]

def is_valid_event(event):
    if not isinstance(event, dict):
        return False

    for field in REQUIRED_EVENT_FIELDS:
        if field not in event:
            return False

    return isinstance(event["payload"], dict)