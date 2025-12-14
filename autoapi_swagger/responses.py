from typing import Any, Dict, Optional, Type
from rest_framework import serializers
from autoapi_swagger.constants import (
    STATUS_CODES, JSEND_SCHEMA, ERROR_RESPONSES,
    SUCCESS_RESPONSES, CONTENT_TYPE_JSON
)


def build_jsend_schema() -> Dict[str, Any]:
    return {
        'JSendError': {
            **JSEND_SCHEMA,
            'properties': {
                **JSEND_SCHEMA['properties'],
                'data': {'type': 'object', 'description': 'Error details'}
            }
        },
        'JSendSuccess': {
            **JSEND_SCHEMA,
            'properties': {
                'status': {'type': 'string', 'enum': ['success'], 'example': 'success'},
                'data': {'type': 'object', 'description': 'Response data'}
            },
            'required': ['status', 'data']
        }
    }


def build_success_response(
    schema_ref: Optional[str] = None,
    status_code: str = STATUS_CODES['success'],
    is_list: bool = False
) -> Dict[str, Any]:
    response = SUCCESS_RESPONSES.get(status_code, SUCCESS_RESPONSES['200']).copy()
    
    if schema_ref:
        data_schema = {'type': 'array', 'items': {'$ref': schema_ref}} if is_list else {'$ref': schema_ref}
        schema = {
            'allOf': [
                {'$ref': '#/components/schemas/JSendSuccess'},
                {'properties': {'data': data_schema}}
            ]
        }
    else:
        schema = {'$ref': '#/components/schemas/JSendSuccess'}
    
    response['content'] = {CONTENT_TYPE_JSON: {'schema': schema}}
    return response


def build_error_responses() -> Dict[str, Any]:
    return ERROR_RESPONSES.copy()


def build_responses(
    serializer_class: Optional[Type[serializers.Serializer]] = None,
    model_class: Optional[Any] = None,
    method: str = 'get',
    action_name: Optional[str] = None
) -> Dict[str, Any]:
    responses = {}
    
    if method == 'delete':
        responses[STATUS_CODES['no_content']] = SUCCESS_RESPONSES['204']
        responses.update(build_error_responses())
        return responses
    
    schema_ref = None
    if serializer_class:
        schema_ref = f"#/components/schemas/{serializer_class.__name__}"
    elif model_class:
        schema_ref = f"#/components/schemas/{model_class.__name__}"
    
    status_code = STATUS_CODES['created'] if method == 'post' else STATUS_CODES['success']
    is_list = method == 'get' and action_name == 'list'
    
    responses[status_code] = build_success_response(schema_ref, status_code, is_list)
    responses.update(build_error_responses())
    
    return responses

