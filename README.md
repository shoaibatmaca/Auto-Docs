# autoapi-swagger

Automatic OpenAPI 3.0 documentation generator for Django REST Framework. This package auto-inspects your DRF views and serializers to generate comprehensive API documentation without requiring manual configuration or docstrings.

## Features

- **OpenAPI 3.0 Support**: Generates modern OpenAPI 3.0 schemas (not limited to 2.0 like drf-yasg)
- **Automatic Introspection**: Auto-discovers views, serializers, and models from your Django project
- **Zero Configuration**: Works out of the box with minimal setup
- **Swagger UI Integration**: Built-in Swagger UI for interactive API exploration
- **Backend Only**: Pure Python package with no frontend dependencies in your project

## Installation

```bash
pip install autoapi-swagger
```

## Quick Start

### 1. Add to INSTALLED_APPS

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'autoapi_swagger',
]
```

### 2. Include URLs

In your main `urls.py`:

```python
from django.urls import path, include
from autoapi_swagger.urls import get_urls

urlpatterns = [
    path('api/', include('your_app.urls')),
    path('', include(get_urls())),
]
```

Or with custom configuration:

```python
from django.urls import path, include
from autoapi_swagger.urls import get_urls

urlpatterns = [
    path('api/', include('your_app.urls')),
    path('docs/', include(get_urls(
        title='My API',
        version='2.0.0',
        description='API documentation for My Project',
        schema_url='openapi.json',
        ui_url='swagger/',
    ))),
]
```

### 3. Access Documentation

- **OpenAPI Schema JSON**: `http://localhost:8000/openapi.json`
- **Swagger UI**: `http://localhost:8000/swagger/`

## Advanced Usage

### Custom Schema View

```python
from autoapi_swagger import get_schema_view
from django.urls import path

schema_view = get_schema_view(
    title='My API',
    version='2.0.0',
    description='Custom API documentation',
    servers=[{'url': 'https://api.example.com', 'description': 'Production'}],
)

urlpatterns = [
    path('openapi.json', schema_view, name='openapi-schema'),
]
```

### Programmatic Schema Access

```python
from autoapi_swagger import get_openapi_schema

schema = get_openapi_schema(
    title='My API',
    version='1.0.0',
    description='API documentation',
)
```

## How It Works

The package automatically:

1. **Discovers URL patterns** from your Django URL configuration
2. **Identifies DRF views** (APIView, ViewSet, etc.)
3. **Extracts serializers** from view classes
4. **Infers request/response schemas** from serializers and models
5. **Maps HTTP methods** to OpenAPI operations
6. **Generates OpenAPI 3.0 schema** with all endpoints, parameters, and schemas

## Comparison with Other Tools

- **drf-yasg**: Limited to OpenAPI 2.0/Swagger, requires more configuration
- **drf-spectacular**: OpenAPI 3.0 support but requires docstrings and configuration for best results
- **autoapi-swagger**: OpenAPI 3.0 with zero configuration, pure auto-introspection

## Requirements

- Python 3.10+
- Django 4.2+
- Django REST Framework 3.12+

## License

MIT
