from typing import Any, Dict, Optional
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from autoapi_swagger.docs_generator import get_openapi_schema
from autoapi_swagger.constants import DEFAULT_TITLE, DEFAULT_VERSION, SWAGGER_UI_VERSION


def get_swagger_ui_html(schema_url: str) -> str:
    return f'''<!DOCTYPE html>
<html>
<head>
    <title>Swagger UI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@{SWAGGER_UI_VERSION}/swagger-ui.css" />
    <style>
        html {{ box-sizing: border-box; overflow-y: scroll; }}
        *, *:before, *:after {{ box-sizing: inherit; }}
        body {{ margin: 0; background: #fafafa; }}
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@{SWAGGER_UI_VERSION}/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@{SWAGGER_UI_VERSION}/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {{
            SwaggerUIBundle({{
                url: "{schema_url}",
                dom_id: '#swagger-ui',
                presets: [SwaggerUIBundle.presets.apis, SwaggerUIStandalonePreset],
                layout: "StandaloneLayout"
            }});
        }};
    </script>
</body>
</html>'''


class OpenAPISchemaView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = kwargs.get('title', DEFAULT_TITLE)
        self.version = kwargs.get('version', DEFAULT_VERSION)
        self.description = kwargs.get('description', '')
        self.servers = kwargs.get('servers', None)
    
    def get(self, request):
        return Response(get_openapi_schema(
            title=self.title,
            version=self.version,
            description=self.description,
            servers=self.servers,
        ))


@require_http_methods(["GET"])
def swagger_ui_view(request, schema_url='openapi.json'):
    return HttpResponse(get_swagger_ui_html(schema_url), content_type='text/html')


def get_schema_view(
    title: str = DEFAULT_TITLE,
    version: str = DEFAULT_VERSION,
    description: str = '',
    servers: Optional[list] = None,
    url: str = 'openapi.json',
    public: bool = True,
):
    view = OpenAPISchemaView.as_view(
        title=title, version=version, description=description, servers=servers
    )
    return method_decorator(cache_page(60 * 15))(view) if not public else view

