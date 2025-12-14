from typing import Any, Dict, List, Optional, Type
from django.urls import URLPattern, URLResolver
from rest_framework import serializers, viewsets, views
from autoapi_swagger.constants import DETAIL_ACTIONS, ACTION_METHOD_MAP


def get_serializer_fields(serializer_class: Type[serializers.Serializer]) -> Dict[str, Any]:
    if not issubclass(serializer_class, serializers.Serializer):
        return {}
    
    fields = {}
    serializer = serializer_class()
    
    for field_name, field in serializer.fields.items():
        field_type_info = get_field_type(field)
        field_info = {
            'type': field_type_info['type'],
            'required': field.required,
        }
        
        if 'format' in field_type_info:
            field_info['format'] = field_type_info['format']
        
        if hasattr(field, 'help_text') and field.help_text:
            field_info['description'] = str(field.help_text)
        
        if hasattr(field, 'default') and field.default != serializers.empty:
            field_info['default'] = field.default
        
        if isinstance(field, serializers.ChoiceField):
            field_info['enum'] = list(field.choices.values()) if hasattr(field, 'choices') else []
        
        fields[field_name] = field_info
    
    return fields


def get_field_type(field: serializers.Field) -> Dict[str, Any]:
    field_type_map = {
        serializers.CharField: {'type': 'string'},
        serializers.IntegerField: {'type': 'integer'},
        serializers.FloatField: {'type': 'number'},
        serializers.DecimalField: {'type': 'number'},
        serializers.BooleanField: {'type': 'boolean'},
        serializers.DateField: {'type': 'string', 'format': 'date'},
        serializers.DateTimeField: {'type': 'string', 'format': 'date-time'},
        serializers.TimeField: {'type': 'string', 'format': 'time'},
        serializers.EmailField: {'type': 'string', 'format': 'email'},
        serializers.URLField: {'type': 'string', 'format': 'uri'},
        serializers.UUIDField: {'type': 'string', 'format': 'uuid'},
        serializers.JSONField: {'type': 'object'},
        serializers.FileField: {'type': 'string', 'format': 'binary'},
        serializers.ImageField: {'type': 'string', 'format': 'binary'},
    }
    
    for field_class, type_info in field_type_map.items():
        if isinstance(field, field_class):
            return type_info.copy()
    
    if isinstance(field, serializers.ListSerializer):
        return {'type': 'array'}
    
    if isinstance(field, serializers.Serializer):
        return {'type': 'object'}
    
    return {'type': 'string'}


def get_view_actions(view_class: Type[Any]) -> Dict[str, Dict[str, Any]]:
    actions = {}
    
    action_map = {
        viewsets.ModelViewSet: ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy'],
        viewsets.ReadOnlyModelViewSet: ['list', 'retrieve'],
    }
    
    base_actions = next((actions for vs, actions in action_map.items() if issubclass(view_class, vs)), [])
    
    for action in base_actions:
        if hasattr(view_class, action):
            actions[action] = {
                'method': ACTION_METHOD_MAP.get(action, 'GET'),
                'detail': action in DETAIL_ACTIONS
            }
    
    try:
        if hasattr(view_class, 'get_extra_actions'):
            for action in view_class.get_extra_actions():
                action_name = getattr(action, 'url_name', None) or getattr(action, 'name', 'unknown')
                actions[action_name] = {
                    'method': action.methods[0] if action.methods else 'GET',
                    'detail': getattr(action, 'detail', False)
                }
    except (AttributeError, TypeError):
        pass
    
    return actions


def get_view_serializer(view_class: Type[Any]) -> Optional[Type[serializers.Serializer]]:
    if hasattr(view_class, 'serializer_class'):
        return view_class.serializer_class
    
    return None


def get_view_queryset_model(view_class: Type[Any]) -> Optional[Type[Any]]:
    if hasattr(view_class, 'get_queryset'):
        queryset = view_class.get_queryset()
        if queryset is not None and hasattr(queryset, 'model'):
            return queryset.model
    
    if hasattr(view_class, 'queryset') and view_class.queryset is not None:
        return view_class.queryset.model
    
    return None


def extract_url_patterns(urlpatterns: List[Any], prefix: str = '') -> List[Dict[str, Any]]:
    patterns = []
    
    for pattern in urlpatterns:
        if isinstance(pattern, URLPattern):
            callback = pattern.callback
            if hasattr(callback, 'cls'):
                view_class = callback.cls
                url_path = prefix + str(pattern.pattern)
                patterns.append({
                    'path': url_path,
                    'view_class': view_class,
                    'name': pattern.name or '',
                })
        elif isinstance(pattern, URLResolver):
            new_prefix = prefix + str(pattern.pattern)
            patterns.extend(extract_url_patterns(pattern.url_patterns, new_prefix))
    
    return patterns


def get_model_fields(model_class: Type[Any]) -> Dict[str, Any]:
    if not hasattr(model_class, '_meta'):
        return {}
    
    fields = {}
    meta = model_class._meta
    
    for field in meta.get_fields():
        if field.name in ['id', 'pk']:
            continue
        
        model_field_type_info = get_model_field_type(field)
        field_info = {
            'type': model_field_type_info['type'],
            'required': not field.null and not hasattr(field, 'blank') or not field.blank,
        }
        
        if 'format' in model_field_type_info:
            field_info['format'] = model_field_type_info['format']
        
        if hasattr(field, 'help_text') and field.help_text:
            field_info['description'] = str(field.help_text)
        
        if hasattr(field, 'default') and field.default is not None:
            if callable(field.default):
                continue
            field_info['default'] = field.default
        
        fields[field.name] = field_info
    
    return fields


def get_model_field_type(field: Any) -> Dict[str, Any]:
    from django.db import models
    
    field_type_map = {
        models.CharField: {'type': 'string'},
        models.TextField: {'type': 'string'},
        models.IntegerField: {'type': 'integer'},
        models.BigIntegerField: {'type': 'integer'},
        models.SmallIntegerField: {'type': 'integer'},
        models.PositiveIntegerField: {'type': 'integer'},
        models.FloatField: {'type': 'number'},
        models.DecimalField: {'type': 'number'},
        models.BooleanField: {'type': 'boolean'},
        models.DateField: {'type': 'string', 'format': 'date'},
        models.DateTimeField: {'type': 'string', 'format': 'date-time'},
        models.TimeField: {'type': 'string', 'format': 'time'},
        models.EmailField: {'type': 'string', 'format': 'email'},
        models.URLField: {'type': 'string', 'format': 'uri'},
        models.UUIDField: {'type': 'string', 'format': 'uuid'},
        models.JSONField: {'type': 'object'},
        models.FileField: {'type': 'string', 'format': 'binary'},
        models.ImageField: {'type': 'string', 'format': 'binary'},
    }
    
    field_type = type(field)
    for model_field_class, type_info in field_type_map.items():
        if issubclass(field_type, model_field_class):
            return type_info.copy()
    
    return {'type': 'string'}

