# Event Definitions

## Shared Event Schema
All events follow this structure:

- event_id: unique ID for the event
- topic: semantic event type
- timestamp: ISO-8601 creation time
- payload: event-specific data

## Event 1: image.submitted
- Publisher: CLI Service
- Subscriber: Inference Service
- Purpose: begin processing pipeline

Payload:
- image_id
- path
- source

## Event 2: inference.completed
- Publisher: Inference Service
- Subscriber: Document Service
- Purpose: pass simulated annotations forward

Payload:
- image_id
- objects
- model_version

## Event 3: annotation.stored
- Publisher: Document Service
- Subscriber: downstream service or logger
- Purpose: confirm annotation storage

Payload:
- image_id
- status
- document_id