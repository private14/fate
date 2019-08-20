from rest_framework import viewsets
from rest_framework import generics
from Fate.serializer import *
from data_migration.views import *

from rest_framework.views import APIView
from rest_framework.schemas.openapi import AutoSchema


class CustomSchema(AutoSchema):
    def get_link(self):
        pass


# Implement custom introspection here (or in other sub-methods)

class CustomView(APIView):
    """APIView subclass with custom schema introspection."""
    schema = CustomSchema()



class EnvViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Env.objects.all()
    serializer_class = EnvSerializer


class CopyDataViewSet(generics.GenericAPIView):
    """
    A simple ViewSet for listing or retrieving users.
    """
    queryset = CopyProduct.objects.all()
    serializer_class = CopyProductSerializer

    def get(self, request):
        # 获取传入参数
        id = request.GET.get('id', '')
        env = request.GET.get('env', '')
        source = request.GET.get('source', '')
        return Response(id)