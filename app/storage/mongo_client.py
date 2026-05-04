import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError


load_dotenv()


class MongoAnnotationStore:
    def __init__(self):
        uri = os.getenv("MONGODB_URI")
        db_name = os.getenv("MONGODB_DB_NAME", "image_annotation_retrieval")

        if not uri:
            raise ValueError("MONGODB_URI is not set. Add it to your .env file.")

        self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        self.db = self.client[db_name]
        self.annotations = self.db["annotations"]

        self.annotations.create_index(
            [("image_id", ASCENDING)],
            unique=True
        )

    def ping(self):
        self.client.admin.command("ping")
        return True

    def store_annotation(self, image_id, objects, model_version="sim_v1"):
        document = {
            "image_id": image_id,
            "objects": objects,
            "model_version": model_version,
            "status": "stored",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "history": [
                "image.submitted",
                "inference.completed",
                "annotation.stored"
            ]
        }

        result = self.annotations.update_one(
            {"image_id": image_id},
            {"$setOnInsert": document},
            upsert=True
        )

        return {
            "image_id": image_id,
            "inserted": result.upserted_id is not None,
            "document_id": f"doc_{image_id}"
        }

    def get_annotation(self, image_id):
        return self.annotations.find_one(
            {"image_id": image_id},
            {"_id": 0}
        )

    def clear_test_data(self):
        self.annotations.delete_many({
            "image_id": {"$regex": "^test_"}
        })