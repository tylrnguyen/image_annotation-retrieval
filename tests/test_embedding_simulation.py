from app.simulation.image_processing import simulate_embedding


def test_embedding_dimension():
    embedding = simulate_embedding("img_test", dimension=128)

    assert len(embedding) == 128


def test_embedding_is_deterministic():
    emb1 = simulate_embedding("img_test", dimension=128)
    emb2 = simulate_embedding("img_test", dimension=128)

    assert emb1 == emb2