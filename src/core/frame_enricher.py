from src.core.models import EnrichedFrame

DEFAULT_COLOR = [1.0, 1.0, 1.0]


class FrameEnricher:

    def __init__(self, color_store):
        self.color_store = color_store

    async def handle_light(self, light_message):

        await self.color_store.set_color(
            light_message["roomId"],
            light_message["newColor"],
        )

    async def handle_frame(self, frame_message):

        color = await self.color_store.get_color(frame_message["roomId"])

        if color is None:
            color = DEFAULT_COLOR

        return EnrichedFrame(
            roomId=frame_message["roomId"],
            cameraId=frame_message["cameraId"],
            frame=frame_message["frame"],
            timestamp=frame_message["timestamp"],
            color=color,
        )
