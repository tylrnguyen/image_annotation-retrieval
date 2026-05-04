import hashlib
import random


def simulate_object_detection(image_id, image_path):
    seed = int(hashlib.sha256(image_id.encode()).hexdigest(), 16) % (10**8)
    rng = random.Random(seed)

    labels = ["car", "person", "dog", "tree", "bike"]

    objects = []
    for i in range(rng.randint(1, 3)):
        objects.append({
            "object_id": f"{image_id}_obj_{i}",
            "label": rng.choice(labels),
            "bbox": [
                rng.randint(0, 100),
                rng.randint(0, 100),
                rng.randint(120, 300),
                rng.randint(120, 300),
            ],
            "conf": round(rng.uniform(0.70, 0.99), 2)
        })

    return objects


def simulate_embedding(image_id, dimension=128):
    seed = int(hashlib.sha256(image_id.encode()).hexdigest(), 16) % (10**8)
    rng = random.Random(seed)

    vector = [rng.random() for _ in range(dimension)]
    norm = sum(x * x for x in vector) ** 0.5

    return [x / norm for x in vector]