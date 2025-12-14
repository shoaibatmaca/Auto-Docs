import unittest
import importlib.util
from pathlib import Path

# Import constants directly without triggering package __init__
constants_path = Path(__file__).parent.parent / 'autoapi_swagger' / 'constants.py'
spec = importlib.util.spec_from_file_location('constants', constants_path)
constants = importlib.util.module_from_spec(spec)
spec.loader.exec_module(constants)


class ConstantsTestCase(unittest.TestCase):
    """Pure Python tests for constants - no Django/DRF dependencies"""
    
    def test_openapi_version(self):
        self.assertEqual(constants.OPENAPI_VERSION, '3.0.0')
    
    def test_default_title(self):
        self.assertEqual(constants.DEFAULT_TITLE, 'API Documentation')
    
    def test_default_version(self):
        self.assertEqual(constants.DEFAULT_VERSION, '1.0.0')
    
    def test_default_server(self):
        self.assertIn('url', constants.DEFAULT_SERVER)
        self.assertIn('description', constants.DEFAULT_SERVER)
        self.assertEqual(constants.DEFAULT_SERVER['url'], '/')
    
    def test_action_method_map(self):
        self.assertEqual(constants.ACTION_METHOD_MAP['list'], 'GET')
        self.assertEqual(constants.ACTION_METHOD_MAP['create'], 'POST')
        self.assertEqual(constants.ACTION_METHOD_MAP['retrieve'], 'GET')
        self.assertEqual(constants.ACTION_METHOD_MAP['update'], 'PUT')
        self.assertEqual(constants.ACTION_METHOD_MAP['partial_update'], 'PATCH')
        self.assertEqual(constants.ACTION_METHOD_MAP['destroy'], 'DELETE')
    
    def test_status_codes(self):
        self.assertEqual(constants.STATUS_CODES['success'], '200')
        self.assertEqual(constants.STATUS_CODES['created'], '201')
        self.assertEqual(constants.STATUS_CODES['no_content'], '204')
        self.assertEqual(constants.STATUS_CODES['bad_request'], '400')
        self.assertEqual(constants.STATUS_CODES['not_found'], '404')
        self.assertEqual(constants.STATUS_CODES['server_error'], '500')
    
    def test_jsend_schema_structure(self):
        self.assertIn('type', constants.JSEND_SCHEMA)
        self.assertIn('properties', constants.JSEND_SCHEMA)
        self.assertIn('status', constants.JSEND_SCHEMA['properties'])
        self.assertIn('data', constants.JSEND_SCHEMA['properties'])
        self.assertIn('message', constants.JSEND_SCHEMA['properties'])
        self.assertIn('code', constants.JSEND_SCHEMA['properties'])
        self.assertIn('required', constants.JSEND_SCHEMA)
        self.assertIn('status', constants.JSEND_SCHEMA['required'])
    
    def test_error_responses_structure(self):
        self.assertIn('400', constants.ERROR_RESPONSES)
        self.assertIn('404', constants.ERROR_RESPONSES)
        self.assertIn('500', constants.ERROR_RESPONSES)
        self.assertEqual(constants.ERROR_RESPONSES['400']['description'], 'Bad Request')
        self.assertEqual(constants.ERROR_RESPONSES['404']['description'], 'Not Found')
        self.assertEqual(constants.ERROR_RESPONSES['500']['description'], 'Internal Server Error')
    
    def test_success_responses(self):
        self.assertIn('200', constants.SUCCESS_RESPONSES)
        self.assertIn('201', constants.SUCCESS_RESPONSES)
        self.assertIn('204', constants.SUCCESS_RESPONSES)
        self.assertEqual(constants.SUCCESS_RESPONSES['200']['description'], 'Success')
        self.assertEqual(constants.SUCCESS_RESPONSES['201']['description'], 'Created')
        self.assertEqual(constants.SUCCESS_RESPONSES['204']['description'], 'No Content')
    
    def test_http_methods(self):
        self.assertIn('get', constants.HTTP_METHODS)
        self.assertIn('post', constants.HTTP_METHODS)
        self.assertIn('put', constants.HTTP_METHODS)
        self.assertIn('delete', constants.HTTP_METHODS)
    
    def test_detail_actions(self):
        self.assertIn('retrieve', constants.DETAIL_ACTIONS)
        self.assertIn('update', constants.DETAIL_ACTIONS)
        self.assertIn('partial_update', constants.DETAIL_ACTIONS)
        self.assertIn('destroy', constants.DETAIL_ACTIONS)
        self.assertNotIn('list', constants.DETAIL_ACTIONS)
        self.assertNotIn('create', constants.DETAIL_ACTIONS)
    
    def test_write_methods(self):
        self.assertIn('post', constants.WRITE_METHODS)
        self.assertIn('put', constants.WRITE_METHODS)
        self.assertIn('patch', constants.WRITE_METHODS)
        self.assertNotIn('get', constants.WRITE_METHODS)
        self.assertNotIn('delete', constants.WRITE_METHODS)
    
    def test_swagger_ui_version(self):
        self.assertEqual(constants.SWAGGER_UI_VERSION, '4.15.5')
    
    def test_content_type_json(self):
        self.assertEqual(constants.CONTENT_TYPE_JSON, 'application/json')
