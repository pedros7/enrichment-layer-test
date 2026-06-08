from src.core.interfaces import ColorStore


class InMemoryColorStore(ColorStore):

    def __init__(self):
        self._colors = {}

    async def get_color(self, room_id: str):
        return self._colors.get(room_id)

    async def set_color(self, room_id: str, color):
        self._colors[room_id] = color
