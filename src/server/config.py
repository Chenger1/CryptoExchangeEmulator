from typing import Optional
from dataclasses import dataclass
from asyncio import Queue


@dataclass
class Config:
    EXCHANGE: Optional[str] = None
    QUEUE: Queue = Queue()
    interface_port: Optional[int] = None
    listener_port: Optional[int] = None
