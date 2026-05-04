from app.broker import Broker
from app.events import EMBEDDING_CREATED, is_valid_event
from app.storage.faiss_index import FaissVectorIndex


broker = Broker()
vector_index = FaissVectorIndex(dimension=128)


def handle_embedding_created(event):
    if not is_valid_event(event):
        print("Vector Index Service: invalid event")
        return

    print("Vector Index Service received:", {
        "event_id": event.get("event_id"),
        "topic": event.get("topic"),
        "image_id": event.get("payload", {}).get("image_id")
    })

    payload = event.get("payload", {})
    image_id = payload.get("image_id")
    embedding = payload.get("embedding")

    if not image_id or embedding is None:
        print("Vector Index Service: missing image_id or embedding")
        return

    try:
        vector_index.add_embedding(image_id, embedding)
    except ValueError as error:
        print(f"Vector Index Service: {error}")
        return

    print(
        f"Vector Index Service indexed {image_id}. "
        f"Total vectors: {vector_index.count()}"
    )


def start():
    broker.subscribe(EMBEDDING_CREATED, handle_embedding_created)
    print("Vector Index Service is running and subscribed to embedding.created...")