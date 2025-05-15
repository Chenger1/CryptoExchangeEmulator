import asyncio
from typing import Any
from collections.abc import AsyncGenerator

import anyio
from litestar import (
    WebSocket,
    websocket
)
from litestar.exceptions import WebSocketDisconnect
from litestar.handlers import send_websocket_stream
from litestar.di import Provide
from loguru import logger

from src.services.exchange_auth import (
    get_exchange_auth,
    ExchangeAuthProtocol,
)
from src.server.config import Config


@websocket('/ws', dependencies={'exchange_auth': Provide(get_exchange_auth, sync_to_thread=False)})
async def ws_handler(socket: WebSocket, exchange_auth: ExchangeAuthProtocol) -> None:
    await socket.accept()
    should_stop = anyio.Event()

    async def handle_stream() -> AsyncGenerator[str, None]:
        while not should_stop.is_set():
            await anyio.sleep(1)
            try:
                data = await Config.QUEUE.get()
                if data.get('port') and data.get('port') == socket.client.port:
                    yield data['data']
                else:
                    await Config.QUEUE.put(data)
            except asyncio.QueueEmpty:
                continue

    async def handle_receive() -> Any:
        await socket.send_json({"handle_receive": "start"})
        async for event in socket.iter_json():
            logger.info(f'Event: {event}')
            if event.get('topic') == 'userSignal':
                Config.EXCHANGE = event.get('exchange')
                Config.interface_port = socket.client.port
                await Config.QUEUE.put({'port': Config.listener_port, 'data': event['signal']})
            else:
                Config.listener_port = socket.client.port
                response = exchange_auth.response_to_auth_signal(event)
                if response:
                    await socket.send_json(response)

    try:
        async with anyio.create_task_group() as tg:
            tg.start_soon(send_websocket_stream, socket, handle_stream())
            tg.start_soon(handle_receive)
    except WebSocketDisconnect:
        should_stop.set()
