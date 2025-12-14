from django.urls import path
from autoapi_swagger.views import OpenAPISchemaView, swagger_ui_view


def get_urls(
    title: str = 'API Documentation',
    version: str = '1.0.0',
    description: str = '',
    servers: list = None,
    schema_url: str = 'openapi.json',
    ui_url: str = 'swagger/',
):
    schema_view = OpenAPISchemaView.as_view(
        title=title,
        version=version,
        description=description,
        servers=servers,
    )
    
    return [
        path(schema_url, schema_view, name='openapi-schema'),
        path(ui_url, swagger_ui_view, {'schema_url': schema_url}, name='swagger-ui'),
    ]

