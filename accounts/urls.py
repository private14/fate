from django.urls import path
from graphene_django.views import GraphQLView
from Fate.schema import *

urlpatterns = [
    path('account/login/', GraphQLView.as_view(graphiql=True, schema=schema)),
]
