OPENAPI_VERSION = '3.0.0'
DEFAULT_TITLE = 'API Documentation'
DEFAULT_VERSION = '1.0.0'
DEFAULT_SERVER = {'url': '/', 'description': 'Default server'}

HTTP_METHODS = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
DETAIL_ACTIONS = {'retrieve', 'update', 'partial_update', 'destroy'}
WRITE_METHODS = ['post', 'put', 'patch']

ACTION_METHOD_MAP = {
    'list': 'GET',
    'create': 'POST',
    'retrieve': 'GET',
    'update': 'PUT',
    'partial_update': 'PATCH',
    'destroy': 'DELETE',
}

STATUS_CODES = {
    'success': '200',
    'created': '201',
    'no_content': '204',
    'bad_request': '400',
    'not_found': '404',
    'server_error': '500',
}

JSEND_SCHEMA = {
    'type': 'object',
    'properties': {
        'status': {'type': 'string', 'enum': ['success', 'fail', 'error']},
        'data': {'type': 'object'},
        'message': {'type': 'string'},
        'code': {'type': 'integer'},
    },
    'required': ['status'],
}

ERROR_RESPONSES = {
    '400': {
        'description': 'Bad Request',
        'content': {
            'application/json': {
                'schema': {
                    'allOf': [
                        {'$ref': '#/components/schemas/JSendError'},
                        {'example': {'status': 'fail', 'message': 'Validation error', 'data': {}}}
                    ]
                }
            }
        }
    },
    '404': {
        'description': 'Not Found',
        'content': {
            'application/json': {
                'schema': {
                    'allOf': [
                        {'$ref': '#/components/schemas/JSendError'},
                        {'example': {'status': 'fail', 'message': 'Resource not found', 'data': {}}}
                    ]
                }
            }
        }
    },
    '500': {
        'description': 'Internal Server Error',
        'content': {
            'application/json': {
                'schema': {
                    'allOf': [
                        {'$ref': '#/components/schemas/JSendError'},
                        {'example': {'status': 'error', 'message': 'Internal server error', 'code': 500}}
                    ]
                }
            }
        }
    },
}

SUCCESS_RESPONSES = {
    '200': {'description': 'Success'},
    '201': {'description': 'Created'},
    '204': {'description': 'No Content'},
}

SWAGGER_UI_VERSION = '4.15.5'
CONTENT_TYPE_JSON = 'application/json'

