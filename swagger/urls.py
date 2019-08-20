from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework import routers, serializers, viewsets
from swagger.views import *
from data_migration.views import *

router = routers.DefaultRouter()
router.register(r'env', EnvViewSet)
router.register(r'copy', CopyDataViewSet)

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('api/', include(router.urls)),
    path('docs/', schema_view)
]
