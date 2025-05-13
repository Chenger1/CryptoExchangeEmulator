def start_app():
    import os
    from loguru import logger

    logger.info('Starting CryptoExchangeEmulator')

    os.environ.setdefault("LITESTAR_APP", "CryptoExchangeEmulator.src.asgi:app")

    from litestar.__main__ import run_cli as litestar_cli
    litestar_cli()
