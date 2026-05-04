from app.storage.faiss_index import FaissVectorIndex
from app.simulation.image_processing import simulate_embedding


def test_faiss_add_and_count():
    index = FaissVectorIndex(dimension=128)

    embedding = simulate_embedding("img_test", dimension=128)

    index.add_embedding("img_test", embedding)

    assert index.count() == 1


def test_faiss_search_returns_nearest_image():
    index = FaissVectorIndex(dimension=128)

    emb1 = simulate_embedding("img_1", dimension=128)
    emb2 = simulate_embedding("img_2", dimension=128)

    index.add_embedding("img_1", emb1)
    index.add_embedding("img_2", emb2)

    results = index.search(emb1, top_k=1)

    assert len(results) == 1
    assert results[0]["image_id"] == "img_1"


def test_faiss_rejects_wrong_dimension():
    index = FaissVectorIndex(dimension=128)

    bad_embedding = [0.1, 0.2, 0.3]

    try:
        index.add_embedding("img_bad", bad_embedding)
        assert False, "Expected ValueError for wrong dimension"
    except ValueError:
        assert True