# Event-Driven Image Annotation and Retrieval System Architecture

## System Overview

This project implements an event-driven image annotation and retrieval pipeline.

The system uses Redis Pub/Sub as the message bus. Services communicate by publishing and subscribing to events instead of calling each other directly.

The current pipeline is:

```text
image.submitted
  -> inference.completed
  -> annotation.stored
  -> embedding.created
  -> vector indexed in FAISS