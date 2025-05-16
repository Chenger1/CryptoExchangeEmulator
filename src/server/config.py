from typing import Optional
from dataclasses import (
    dataclass,
    field
)
from asyncio import Queue


@dataclass
class _Config:
    EXCHANGE: Optional[str] = None
    WEB_QUEUE: Queue = field(default_factory=Queue)
    SERVICE_QUEUE: Queue = field(default_factory=Queue)


Config = _Config()
