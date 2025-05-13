import os
from pathlib import Path

from dotenv import load_dotenv

from litestar.config.app import AppConfig
from litestar.plugins import InitPlugin
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig
from litestar.static_files import create_static_files_router


load_dotenv()


class ApplicationCore(InitPlugin):
    def _get_template_config(self) -> TemplateConfig:
        return TemplateConfig(
            directory=Path(__file__).parent.parent / 'templates',
            engine=JinjaTemplateEngine
        )

    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        from src.domain.web.controllers import WebController

        app_config.route_handlers.extend([
            create_static_files_router(path='/static', directories=[Path(__file__).parent.parent / 'assets'], name='assets'),
            WebController
        ])

        app_config.template_config = self._get_template_config()
        app_config.debug = os.getenv('DEBUG', default='True') == 'True'

        return app_config
