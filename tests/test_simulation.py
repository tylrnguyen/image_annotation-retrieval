from app.simulation.image_processing import simulate_object_detection, simulate_embedding


def test_object_detection_returns_objects():
    objects = simulate_object_detection("img_test", "images/test.jpg")

    assert len(objects) >= 1
    assert "label" in objects[0]
    assert "bbox" in objects[0]
    assert "conf" in objects[0]


def test_embedding_dimension():
    embedding = simulate_embedding("img_test", dimension=128)

    assert len(embedding) == 128


def test_embedding_is_deterministic():
    emb1 = simulate_embedding("img_test", dimension=128)
    emb2 = simulate_embedding("img_test", dimension=128)

    assert emb1 == emb2