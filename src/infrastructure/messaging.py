import asyncio

from src.core.interfaces import (
    MessageProducer,
    MessageConsumer,
)


class InMemoryTopic:

    def __init__(self):
        self.queue = asyncio.Queue()


class InMemoryProducer(MessageProducer):

    def __init__(self, topic):
        self.topic = topic

    async def publish(self, message):
        await self.topic.queue.put(message)


class InMemoryConsumer(MessageConsumer):

    def __init__(self, topic):
        self.topic = topic

    async def receive(self):
        while True:
            msg = await self.topic.queue.get()
            yield msg
