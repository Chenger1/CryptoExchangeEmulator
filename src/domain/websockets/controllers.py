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
    queue_name = None

    async def handle_stream() -> AsyncGenerator[str, None]:
        while not should_stop.is_set():
            await anyio.sleep(1)
            try:
                print(queue_name)
                if queue_name == 'web':
                    data = await Config.WEB_QUEUE.get()
                elif queue_name == 'service':
                    data = await Config.SERVICE_QUEUE.get()
                else:
                    continue

                yield data['data']
            except asyncio.QueueEmpty:
                continue

    async def handle_receive() -> Any:
        nonlocal queue_name
        async for event in socket.iter_json():
            logger.info(f'Event: {event}')
            if isinstance(event, dict) and event.get('topic') == 'userSignal':
                queue_name = 'web'
                Config.EXCHANGE = event.get('exchange')
                if event['signal'] == 'success':
                    continue
                await Config.SERVICE_QUEUE.put({'data': event['signal']})
            else:
                if Config.EXCHANGE is None:
                    raise ValueError('Exchange is not set')
                queue_name = 'service'
                await Config.WEB_QUEUE.put({'data': json.dumps(event)})

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
