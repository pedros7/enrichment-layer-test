import asyncio

from src.infrastructure.storing import InMemoryColorStore
from src.core.frame_enricher import FrameEnricher


async def demo():

    store = InMemoryColorStore()
    enricher = FrameEnricher(store)

    await enricher.handle_light(
        {
            "roomId": "room-1",
            "newColor": [0.1, 1.0, 0.5],
            "timestamp": "2026-06-01T10:00:00",
        }
    )

    enriched = await enricher.handle_frame(
        {
            "roomId": "room-1",
            "cameraId": "camera-a",
            "frame": "blob",
            "timestamp": "2026-06-01T10:00:01",
        }
    )

    print(enriched)


if __name__ == "__main__":
    asyncio.run(demo())
