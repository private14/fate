from rest_framework import viewsets
from Fate.serializer import *
from data_migration.views import *


class EnvViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Env.objects.all()
    serializer_class = EnvSerializer


class CopyDataViewSet(viewsets.ModelViewSet):
    pass

