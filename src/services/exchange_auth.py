from typing import (
    Protocol,
    runtime_checkable,
    Optional
)

from src.server.config import Config


__all__ = ['get_exchange_auth', 'ExchangeAuthProtocol']


@runtime_checkable
class ExchangeAuthProtocol(Protocol):
    def response_to_auth_signal(self, signal: dict) -> Optional[dict]: ...



class BybitExchangeAuth:
    def response_to_auth_signal(self, signal: dict) -> Optional[dict]:
        topic = signal.get('op')
        if topic == 'auth' or topic == 'subscribe':
            return {
                'success': True,
                'ret_msg': '',
                'op': topic,
                'conn_id': ''
            }
        elif topic == 'ping':
            return {
                'op': 'pong',
                'ret_msg': ''
            }
        return None


class BinanceExchangeAuth:
    def response_to_auth_signal(self, signal: dict) -> Optional[dict]:
        ...


class OKXExchangeAuth:
    def response_to_auth_signal(self, signal: dict) -> Optional[dict]:
        ...


def get_exchange_auth() -> Optional[ExchangeAuthProtocol]:
    if Config.EXCHANGE == 'bybit':
        return BybitExchangeAuth()
    elif Config.EXCHANGE == 'binance':
        return BinanceExchangeAuth()
    elif Config.EXCHANGE == 'okx':
        return OKXExchangeAuth()
    return None
