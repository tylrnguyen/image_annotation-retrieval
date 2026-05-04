IMAGE_SUBMITTED = "image.submitted"
INFERENCE_COMPLETED = "inference.completed"
ANNOTATION_STORED = "annotation.stored"
EMBEDDING_CREATED = "embedding.created"

REQUIRED_EVENT_FIELDS = ["event_id", "topic", "timestamp", "payload"]


def is_valid_event(event):
    if not isinstance(event, dict):
        return False

    for field in REQUIRED_EVENT_FIELDS:
        if field not in event:
            return False

    return isinstance(event["payload"], dict)