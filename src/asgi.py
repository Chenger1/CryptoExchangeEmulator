def create_app():
    from litestar import Litestar

    from src.server.core import ApplicationCore

    return Litestar(plugins=[ApplicationCore()])


app = create_app()
