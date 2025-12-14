import inspect
from typing import Any, Dict, List, Optional, Type
from django.urls import get_resolver
from rest_framework import serializers, viewsets
from autoapi_swagger.constants import OPENAPI_VERSION, DEFAULT_SERVER, WRITE_METHODS
from autoapi_swagger.utils import (
    get_serializer_fields,
    get_view_actions,
    get_view_serializer,
    get_view_queryset_model,
    extract_url_patterns,
    get_model_fields,
)
from autoapi_swagger.responses import build_responses, build_jsend_schema


def get_openapi_schema(
    title: str = 'API Documentation',
    version: str = '1.0.0',
    description: str = '',
    servers: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    urlpatterns = get_resolver().url_patterns
    paths = {}
    components = {'schemas': build_jsend_schema()}
    
    patterns = extract_url_patterns(urlpatterns)
    
    for pattern_info in patterns:
        view_class = pattern_info['view_class']
        if not is_drf_view(view_class):
            continue
        
        path_item = build_path_item(view_class, pattern_info['path'], pattern_info['name'])
        if path_item:
            for path_key, path_operations in path_item.items():
                paths.setdefault(path_key, {}).update(path_operations)
            extract_schemas(view_class, components['schemas'])
    
    return {
        'openapi': OPENAPI_VERSION,
        'info': {
            'title': title,
            'version': version,
            'description': description or f'API documentation for {title}',
        },
        'servers': servers or [DEFAULT_SERVER],
        'paths': paths,
        'components': components,
    }


def is_drf_view(view_class: Type[Any]) -> bool:
    from rest_framework import views
    return (
        inspect.isclass(view_class) and
        (issubclass(view_class, views.APIView) or
         issubclass(view_class, viewsets.ViewSet) or
         hasattr(view_class, 'as_view'))
    )


def build_path_item(view_class: Type[Any], path: str, path_name: str) -> Optional[Dict[str, Any]]:
    path_item = {}
    base_path = normalize_path(path)
    
    if issubclass(view_class, viewsets.ViewSet):
        for action_name, action_info in get_view_actions(view_class).items():
            method = action_info['method'].lower()
            is_detail = action_info.get('detail', False)
            op_path = f"{base_path}/{{id}}/" if is_detail else base_path
            operation = build_operation(view_class, action_name, method, is_detail)
            if operation:
                path_item.setdefault(op_path, {})[method] = operation
    else:
        for method in get_view_methods(view_class):
            operation = build_operation(view_class, None, method, False)
            if operation:
                path_item.setdefault(base_path, {})[method] = operation
    
    return path_item or None


def normalize_path(path: str) -> str:
    path = path.rstrip('$')
    if not path.startswith('/'):
        path = '/' + path
    return path


def get_view_methods(view_class: Type[Any]) -> List[str]:
    from autoapi_swagger.constants import HTTP_METHODS
    return [m for m in HTTP_METHODS if hasattr(view_class, m)]


def build_operation(
    view_class: Type[Any],
    action_name: Optional[str],
    method: str,
    is_detail: bool
) -> Optional[Dict[str, Any]]:
    operation = {
        'summary': get_operation_summary(view_class, action_name, method),
        'operationId': get_operation_id(view_class, action_name, method),
        'tags': [get_view_tag(view_class)],
    }
    
    serializer_class = get_view_serializer(view_class)
    model_class = get_view_queryset_model(view_class)
    
    if is_detail or method in ['put', 'patch', 'delete']:
        operation['parameters'] = [{
            'name': 'id',
            'in': 'path',
            'required': True,
            'schema': {'type': 'integer'},
            'description': 'Resource identifier',
        }]
    
    if method in WRITE_METHODS:
        request_body = build_request_body(serializer_class, model_class)
        if request_body:
            operation['requestBody'] = request_body
    
    operation['responses'] = build_responses(serializer_class, model_class, method, action_name)
    
    return operation


def get_operation_summary(view_class: Type[Any], action_name: Optional[str], method: str) -> str:
    if action_name:
        return action_name.replace('_', ' ').title()
    class_name = view_class.__name__.rstrip('ViewSet').rstrip('View')
    return f"{class_name} {method.upper()}"


def get_operation_id(view_class: Type[Any], action_name: Optional[str], method: str) -> str:
    class_name = view_class.__name__.lower().replace('viewset', '').replace('view', '')
    
    if action_name:
        return f"{class_name}_{action_name}"
    
    return f"{class_name}_{method}"


def get_view_tag(view_class: Type[Any]) -> str:
    return view_class.__name__.rstrip('ViewSet').rstrip('View')


def build_request_body(
    serializer_class: Optional[Type[serializers.Serializer]],
    model_class: Optional[Type[Any]]
) -> Optional[Dict[str, Any]]:
    from autoapi_swagger.constants import CONTENT_TYPE_JSON
    
    schema_name = (serializer_class or model_class).__name__ if (serializer_class or model_class) else None
    if not schema_name:
        return None
    
    return {
        'required': True,
        'content': {
            CONTENT_TYPE_JSON: {'schema': {'$ref': f"#/components/schemas/{schema_name}"}}
        }
    }




def extract_schemas(view_class: Type[Any], schemas: Dict[str, Any]) -> None:
    serializer_class = get_view_serializer(view_class)
    model_class = get_view_queryset_model(view_class)
    
    if serializer_class:
        schema_name = serializer_class.__name__
        if schema_name not in schemas:
            schemas[schema_name] = build_serializer_schema(serializer_class)
    
    if model_class:
        schema_name = model_class.__name__
        if schema_name not in schemas:
            schemas[schema_name] = build_model_schema(model_class)


def build_serializer_schema(serializer_class: Type[serializers.Serializer]) -> Dict[str, Any]:
    schema = {'type': 'object', 'properties': {}, 'required': []}
    
    for field_name, field_info in get_serializer_fields(serializer_class).items():
        prop = {'type': field_info['type']}
        for key in ['format', 'description', 'default', 'enum']:
            if key in field_info:
                prop[key] = field_info[key]
        schema['properties'][field_name] = prop
        if field_info['required']:
            schema['required'].append(field_name)
    
    return schema


def build_model_schema(model_class: Type[Any]) -> Dict[str, Any]:
    schema = {
        'type': 'object',
        'properties': {'id': {'type': 'integer', 'description': 'Primary key'}},
        'required': [],
    }
    
    for field_name, field_info in get_model_fields(model_class).items():
        prop = {'type': field_info['type']}
        for key in ['format', 'description', 'default']:
            if key in field_info:
                prop[key] = field_info[key]
        schema['properties'][field_name] = prop
        if field_info['required']:
            schema['required'].append(field_name)
    
    return schema

