from abc import ABC, abstractmethod


class ColorStore(ABC):

    @abstractmethod
    async def get_color(self, room_id: str):
        pass

    @abstractmethod
    async def set_color(self, room_id: str, color):
        pass


class MessageProducer(ABC):

    @abstractmethod
    async def publish(self, message: dict):
        pass


class MessageConsumer(ABC):

    @abstractmethod
    async def receive(self):
        pass
