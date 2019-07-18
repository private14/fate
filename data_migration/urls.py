from django.urls import path
from data_migration.views import *

urlpatterns = [
    path('merchant/', DataView.copy_merchant_id),
]
