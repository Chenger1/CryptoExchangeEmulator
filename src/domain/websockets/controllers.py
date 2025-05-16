import json
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
from loguru import logger

from src.services.exchange_auth import (
    get_exchange_auth,
    ExchangeAuthProtocol,
)
from src.server.config import Config


@websocket('/ws')
async def ws_handler(socket: WebSocket) -> None:
    await socket.accept()
    should_stop = anyio.Event()
    Config.CLIENTS.append(socket.client.port)

    async def handle_stream() -> AsyncGenerator[str, None]:
        while not should_stop.is_set():
            await anyio.sleep(1)
            try:
                data = await Config.QUEUE.get()
                if socket.client.port not in data['proceeded_clients']:
                    data['proceeded_clients'].append(socket.client.port)
                    yield json.dumps(data['data'])
                    if len(data['proceeded_clients']) != len(Config.CLIENTS):
                        await Config.QUEUE.put(data)
            except asyncio.QueueEmpty:
                continue

    async def handle_receive() -> Any:
        async for event in socket.iter_json():
            logger.info(f'Event: {event}')
            if isinstance(event, dict) and event.get('topic') == 'userSignal':
                Config.EXCHANGE = event.get('exchange')
                await Config.QUEUE.put({'data': event['signal'], 'proceeded_clients': []})
            else:
                if Config.EXCHANGE is None:
                    raise ValueError('Exchange is not set')
                await Config.QUEUE.put({'data': event, 'proceeded_clients': []})

                exchange_auth: ExchangeAuthProtocol = get_exchange_auth()
                response = exchange_auth.response_to_auth_signal(event)
                if response:
                    if isinstance(response, str):
                        await socket.send_text(response)
                    else:
                        await socket.send_json(response)

    try:
        async with anyio.create_task_group() as tg:
            tg.start_soon(send_websocket_stream, socket, handle_stream())
            tg.start_soon(handle_receive)
    except WebSocketDisconnect:
        should_stop.set()
