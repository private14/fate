from django.urls import path
from common_function.views import *

urlpatterns = [
    path('random/', RandomListView.get),
    path('jenkins/', JenkinsView.get),
]
