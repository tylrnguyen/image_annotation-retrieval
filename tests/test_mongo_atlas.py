import os
import pytest

from app.storage.mongo_client import MongoAnnotationStore


@pytest.mark.skipif(
    not os.getenv("MONGODB_URI"),
    reason="MONGODB_URI not set"
)
def test_mongo_atlas_connection():
    store = MongoAnnotationStore()
    assert store.ping() is True


@pytest.mark.skipif(
    not os.getenv("MONGODB_URI"),
    reason="MONGODB_URI not set"
)
def test_mongo_atlas_store_annotation_idempotent():
    store = MongoAnnotationStore()

    image_id = "test_img_atlas_001"

    store.store_annotation(
        image_id=image_id,
        objects=[{"label": "car", "conf": 0.9}],
        model_version="sim_v1"
    )

    second = store.store_annotation(
        image_id=image_id,
        objects=[{"label": "car", "conf": 0.9}],
        model_version="sim_v1"
    )

    saved = store.get_annotation(image_id)

    assert saved["image_id"] == image_id
    assert second["inserted"] is False

    store.clear_test_data()