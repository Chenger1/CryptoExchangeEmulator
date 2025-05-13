def create_app():
    import os
    from pathlib import Path

    from dotenv import load_dotenv
    from litestar import Litestar
    from litestar.static_files import create_static_files_router
    from litestar.contrib.jinja import JinjaTemplateEngine
    from litestar.template.config import TemplateConfig

    load_dotenv()

    return Litestar(
        route_handlers=[
            create_static_files_router(path='/static', directories=[Path(__file__).parent / 'assets'], name='assets')
        ],
        template_config=TemplateConfig(
            directory=Path(__file__).parent / 'templates',
            engine=JinjaTemplateEngine
        ),
        debug=os.getenv('DEBUG', default='True') == 'True'
    )


app = create_app()
