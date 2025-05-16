from typing import (
    Protocol,
    runtime_checkable,
    Optional,
    Union
)

from src.server.config import Config


__all__ = ['get_exchange_auth', 'ExchangeAuthProtocol']


@runtime_checkable
class ExchangeAuthProtocol(Protocol):
    def response_to_auth_signal(self, signal: Union[dict, str]) -> Optional[Union[dict, str]]: ...



class BybitExchangeAuth:
    def response_to_auth_signal(self, signal: Union[dict, str]) -> Optional[Union[dict, str]]:
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
    def response_to_auth_signal(self, signal: Union[dict, str]) -> Optional[Union[dict, str]]:
        # Binance does not require special response
        ...


class OKXExchangeAuth:
    def response_to_auth_signal(self, signal: Union[dict, str]) -> Optional[Union[dict, str]]:
        if signal == 'ping':
            return 'pong'

        topic = signal.get('op')
        if topic == 'login':
            return {
                'event': 'login',
                'msg': '',
                'code': '0',
                'connId': ''
            }
        elif topic == 'subscribe':
            return {
                'event': 'subscribe',
                'arg': signal['args']
            }
        elif topic == 'ping':
            return {
                'event': 'pong'
            }
        return signal


def get_exchange_auth() -> Optional[ExchangeAuthProtocol]:
    Config.EXCHANGE = 'okx'
    if Config.EXCHANGE == 'bybit':
        return BybitExchangeAuth()
    elif Config.EXCHANGE == 'binance':
        return BinanceExchangeAuth()
    elif Config.EXCHANGE == 'okx':
        return OKXExchangeAuth()
    return None
