from django.test import TestCase
from rest_framework import serializers, viewsets
from rest_framework.test import APIRequestFactory
from autoapi_swagger import get_openapi_schema
from autoapi_swagger.utils import (
    get_serializer_fields,
    get_view_actions,
    get_view_serializer,
    get_view_queryset_model,
)


class TestSerializer(serializers.Serializer):
    name = serializers.CharField(help_text='Name field')
    age = serializers.IntegerField(required=False)
    email = serializers.EmailField()


class TestModel:
    class _meta:
        pass


class TestViewSet(viewsets.ModelViewSet):
    serializer_class = TestSerializer
    
    def get_queryset(self):
        return None


class CoreTestCase(TestCase):
    def test_get_serializer_fields(self):
        fields = get_serializer_fields(TestSerializer)
        self.assertIn('name', fields)
        self.assertIn('age', fields)
        self.assertIn('email', fields)
        self.assertEqual(fields['name']['type'], 'string')
        self.assertEqual(fields['age']['type'], 'integer')
        self.assertFalse(fields['age']['required'])
        self.assertTrue(fields['name']['required'])
    
    def test_get_view_actions(self):
        actions = get_view_actions(TestViewSet)
        self.assertIn('list', actions)
        self.assertIn('create', actions)
        self.assertIn('retrieve', actions)
        self.assertEqual(actions['list']['method'], 'GET')
        self.assertEqual(actions['create']['method'], 'POST')
    
    def test_get_view_serializer(self):
        serializer = get_view_serializer(TestViewSet)
        self.assertEqual(serializer, TestSerializer)
    
    def test_get_openapi_schema(self):
        schema = get_openapi_schema(
            title='Test API',
            version='1.0.0',
        )
        self.assertEqual(schema['openapi'], '3.0.0')
        self.assertEqual(schema['info']['title'], 'Test API')
        self.assertEqual(schema['info']['version'], '1.0.0')
        self.assertIn('paths', schema)
        self.assertIn('components', schema)

