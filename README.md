# Image Annotation Retrieval

[video demo](https://drive.google.com/drive/folders/1ZEolIidaFRVNBDfZ_PlysgSJknEDAJt2?usp=sharing)

An event-driven image processing pipeline that turns an uploaded image into structured annotations, embeddings, and an in-memory vector index.

The services communicate over Redis Pub/Sub and store annotation records in MongoDB while FAISS keeps the embedding index ready for retrieval experiments.

## What It Does

- Accepts an image path from the command line.
- Publishes an `image.submitted` event.
- Simulates inference to produce detected objects.
- Stores annotation metadata in MongoDB with idempotent writes.
- Generates a deterministic embedding from the image id.
- Adds the embedding to a FAISS vector index.

## Pipeline

```text
image.submitted
	-> inference.completed
	-> annotation.stored
	-> embedding.created
	-> FAISS index updated
```

## Project Layout

```text
main.py                         CLI entrypoint
app/
	broker.py                     Redis Pub/Sub wrapper
	events.py                     Shared event and channel constants
	services/                     Pipeline services
	simulation/                   Deterministic image and embedding simulators
	storage/                      MongoDB and FAISS storage adapters
tests/                          Pytest suite
```

## Requirements

- Python 3.14+
- Redis running locally on `localhost:6379`
- MongoDB connection string in `MONGODB_URI` when using the Mongo-backed tests or storage

## Installation

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file if you want to use MongoDB-backed storage:

```env
MONGODB_URI=mongodb://localhost:27017
MONGODB_DB_NAME=image_annotation_retrieval
```

`MONGODB_DB_NAME` is optional and defaults to `image_annotation_retrieval`.

## Run The Pipeline

Use any image path you want to submit:

```bash
python3 main.py images/test.jpg
```

That command starts the services, submits the image, and lets the event chain flow through inference, annotation storage, embedding creation, and vector indexing.

## Tests

Run the full test suite with:

```bash
python3 -m pytest
```

If you do not have `MONGODB_URI` set, the Mongo-backed tests are skipped automatically.

## Notes

- Event names are centralized in `app/events.py` so services and tests share the same constants.
- The simulation layer keeps the pipeline deterministic and easy to test without a real model.
- `tests/test_mongo_atlas.py` should use a valid Python module name if you want pytest to collect it reliably.

