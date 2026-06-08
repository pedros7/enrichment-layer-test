import pytest

from src.infrastructure.storing import InMemoryColorStore
from src.core.frame_enricher import FrameEnricher


@pytest.mark.asyncio
async def test_frame_is_enriched():

    store = InMemoryColorStore()

    await store.set_color(
        "room-1",
        [0.5, 0.4, 0.3],
    )

    enricher = FrameEnricher(store)

    result = await enricher.handle_frame(
        {
            "roomId": "room-1",
            "cameraId": "cam-1",
            "frame": "blob",
            "timestamp": "now",
        }
    )

    assert result.color == [0.5, 0.4, 0.3]
