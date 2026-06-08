import pytest

from src.infrastructure.storing import InMemoryColorStore
from src.core.frame_enricher import FrameEnricher


@pytest.mark.asyncio
async def test_latest_color_wins():

    store = InMemoryColorStore()

    enricher = FrameEnricher(store)

    await enricher.handle_light(
        {
            "roomId": "room-1",
            "newColor": [1, 0, 0],
        }
    )

    await enricher.handle_light(
        {
            "roomId": "room-1",
            "newColor": [0, 1, 0],
        }
    )

    frame = await enricher.handle_frame(
        {
            "roomId": "room-1",
            "cameraId": "cam-1",
            "frame": "blob",
            "timestamp": "now",
        }
    )

    assert frame.color == [0, 1, 0]
