from typing import (
    Optional,
    List
)
from dataclasses import (
    dataclass,
    field
)
from asyncio import Queue


@dataclass
class _Config:
    EXCHANGE: Optional[str] = None
    QUEUE: Queue = field(default_factory=Queue)
    CLIENTS: List = field(default_factory=list)


Config = _Config()
