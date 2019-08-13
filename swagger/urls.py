from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework import routers, serializers, viewsets
from data_migration.views import *


# Serializers define the API representation.
class EnvSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Env
        fields = ('id', 'envName', 'urlDict', 'sqlDict')


# ViewSets define the view behavior.
class EnvViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Return a user instance.
    list:
        Return all users, ordered by most recently joined.
    create:
        Create a new user.
    delete:
        Remove an existing user.
    partial_update:
        Update one or more fields on an existing user.
    update:
        Update a user.
    """
    queryset = User.objects.all()
    serializer_class = EnvSerializer


#class DataViewSet(viewsets.ModelViewSet):


router = routers.DefaultRouter()
router.register(r'env', EnvViewSet)
router.register(r'fate', DataView.copy_merchant_id())

schema_view = get_schema_view(title='Users API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('api/', include(router.urls)),
    path('docs/', schema_view, name='docs')

]
