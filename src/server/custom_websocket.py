from typing import (
    AsyncGenerator,
    Any
)

from litestar import WebSocket
from litestar.types.asgi_types import WebSocketMode
from litestar.serialization import decode_json
from litestar.exceptions import SerializationException


class CustomWebSocket(WebSocket):
    async def iter_json(self, mode: WebSocketMode = 'text') -> AsyncGenerator[Any, None]:
        async for data in self.iter_data(mode):
            try:
                yield decode_json(value=data, type_decoders=self.route_handler.resolve_type_decoders())
            except SerializationException as e:
                if data == 'ping':
                    yield data
                else:
                    raise e
