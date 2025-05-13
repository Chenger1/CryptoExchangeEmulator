from litestar import Controller
from litestar.handlers.websocket_handlers import websocket_listener


class WebsocketController(Controller):
    @websocket_listener('/ws')
    async def handler(self, data: str) -> str:
        print(data)
        return data
