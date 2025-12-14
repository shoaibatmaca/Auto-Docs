from django.urls import path, include
from autoapi_swagger.urls import get_urls

urlpatterns = [
    path('', include(get_urls())),
]

