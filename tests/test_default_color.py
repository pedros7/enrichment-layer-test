import pytest

from src.infrastructure.storing import InMemoryColorStore
from src.core.frame_enricher import (
    FrameEnricher,
    DEFAULT_COLOR,
)


@pytest.mark.asyncio
async def test_default_color_is_used():

    store = InMemoryColorStore()

    enricher = FrameEnricher(store)

    frame = await enricher.handle_frame(
        {
            "roomId": "unknown-room",
            "cameraId": "cam-1",
            "frame": "blob",
            "timestamp": "now",
        }
    )

    assert frame.color == DEFAULT_COLOR
