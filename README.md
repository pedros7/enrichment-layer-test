# Room Light Frame Enricher Service

This project implements a streaming enrichment service that processes camera frames and enriches them with the latest ambient light color of each room.

Each camera produces frames continuously, while each room has a light sensor that occasionally updates the room’s current color. The goal of the system is to ensure that every frame is enriched with the most recent known color for its room before being sent to an inference service.

---

## Core Idea

There are two incoming event streams:
1. **Frames stream** (1 FPS per camera): Contains images from cameras in different rooms.
2. **Light updates** (every ~10–20 minutes per room): Contains the latest RGB color for each room.

**The Golden Rule:** Each frame must be enriched with the latest known color for its room at processing time.

---

## Conceptual Architecture

In production, the system would be built using a distributed streaming architecture:

```text
Cameras ───► Kafka topic: `frames` ─────────┐
                                            ▼
                                 Frame Enrichment Service ───► Kafka topic: `enriched_frames` ───► Inference Service
                                            ▲
RGB Lights ─► Kafka topic: `lights` ────────┘

```


## State Management
The service maintains an optimized, lightweight lookup state:

```text
room_id ──► latest_color
```
This state is updated dynamically whenever a new light event arrives.

## Replaceable Components (Kafka / Redis)
The core infrastructure can be natively swapped out without changing business logic:

### 1. Message Transport Layer (Apache Kafka)
In Production: 
Cameras and lights publish to designated Kafka topics (frames and lights). The service consumes from both streams asynchronously and forwards outputs to enriched_frames.

In This Implementation: 
Replaced by safe in-memory asynchronous queues. The architectural contracts are fully preserved via MessageConsumer and MessageProducer abstract types.

### 2. State Store (Redis Cache)
In Production: Redis acts as a fast, shared, distributed key-value cache holding state metrics across instances:

room-1 ──► [0.1, 1.0, 0.5]

room-2 ──► [0.8, 0.2, 0.3]

In This Implementation: Replaced by a in-memory dictionary store wrapped behind the ColorStore interface contract.

## Key Design Principles
* Stateless Processing Layer: The enrichment nodes have no local persistence, meaning they can scale horizontally effortlessly.

* Single Shared State Per Room: Keeps the memory footprint extremely low (only the absolute latest color array is retained).

* Partitioned Constraints: No global ordering guarantees are needed across different rooms.

* Resilient Throughput: Operates on a best-effort processing model where rare drops or duplicates are gracefully tolerated.

* Sequence Protection: Employs partition key routing strategies to ensure per-camera frame delivery order is strictly preserved.

Project Structure
```text
room-light-enricher/
│
├── src/
│   ├── models.py          # Data structures (frames, lights, output schemas)
│   ├── frame_enricher.py  # Core enrichment business logic
│   ├── stores.py          # In-memory Redis state adapter
│   ├── messaging.py       # In-memory Kafka pub-sub transport adapter
│   ├── interfaces.py      # Abstract contracts (Kafka/Redis swap layer)
│   └── main.py            # Local orchestration & pipeline execution demo
│
└── tests/
    ├── test_enrichment.py     # Verifies frame integration flows
    ├── test_latest_color.py   # Validates that newer state overwrites older metrics
    └── test_default_color.py  # Assures fallback defaults handle unknown rooms gracefully

```

## Operational Mechanics
Light events trigger updates to the stored color per room.

Frame events pull the current color context matching their roomId.

If no light heartbeat has been recorded yet, it attaches a default neutral profile ([1.0, 1.0, 1.0]).

The enriched frame payload is instantly dispatched downstream to the pipeline output.

## How to Run
1. Install dependencies
```
python -m pip install -r requirements.txt
```
2. Run the test suite
```
python -m pytest
```
3. Run the demonstration script
```
python -m src.main
```