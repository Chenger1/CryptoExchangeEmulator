from litestar import (
    Controller,
    get
)
from litestar.response import Template
from litestar.status_codes import HTTP_200_OK


class WebController(Controller):
    include_in_schema = False
    opt = {'exclude_from_auth': True}

    @get(
        path='/',
        operation_id='WebIndex',
        name='frontend:index',
        status_code=HTTP_200_OK,
    )
    async def index(self) -> Template:
        return Template(template_name='index.html.jinja2')
