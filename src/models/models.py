from dataclasses import dataclass
from typing import List


@dataclass
class FrameMessage:
    roomId: str
    cameraId: str
    frame: str
    timestamp: str


@dataclass
class LightMessage:
    roomId: str
    newColor: List[float]
    timestamp: str


@dataclass
class EnrichedFrame:
    roomId: str
    cameraId: str
    frame: str
    timestamp: str
    color: List[float]
