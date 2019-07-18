from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views import View
from accounts.models import *
from django.forms.models import model_to_dict


class DataView(View):

    @api_view(['GET'])
    def copy_merchant_id(request):
        # 获取传入参数
        id = request.GET.get('id', '')
        env = request.GET.get('env', '')
        DataView.copy_merchant_id_by_sit1(env_name=env)
        return Response({'id': id, 'env': env})

    @staticmethod
    def get_modules(env_name):
        sql_dict = Env.objects.filter(envName=env_name)
        return model_to_dict(sql_dict[0])

    @staticmethod
    def copy_merchant_id_by_sit1(env_name):
        sit1_dict = DataView.get_modules('sit1')
        print(sit1_dict)