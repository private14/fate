from rest_framework import viewsets
from Fate.serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views import View
from accounts.models import *
from django.forms.models import model_to_dict
from common_function.operate_sql import *
from rest_framework.views import APIView
from rest_framework.response import Response
from resource_all.resource import *
from common_function.jenkins import *
import json
import datetime


class RandomListViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Env.objects.all()
    serializer_class = RandomListSerializer


class RandomListView(APIView):
    @api_view(['GET'])
    def get(request):
        return RandomListView.randomList()


    @staticmethod
    def randomList():
        random_list = {
            'name': create_name(),
            'phone': create_phone(),
            'identity_card': create_identity_card(risk_control='on'),
            'bank_card': create_bank_card()
        }
        return Response(random_list)


class JenkinsView(APIView):
    @api_view(['GET'])
    def get(request):
        # 获取传入参数
        jenkins_url = request.GET.get('jenkins_url', '')
        username = request.GET.get('username', '')
        password = request.GET.get('password', '')
        params = request.GET.get('params', '')
        job_name = request.GET.get('job_name', '')
        return build_jenkins(jenkins_url, username, password, params, job_name)

