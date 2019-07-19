from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views import View
from accounts.models import *
from django.forms.models import model_to_dict
from common_function.operate_sql import *
import json


class DataView(View):

    @api_view(['GET'])
    def copy_merchant_id(request):
        # 获取传入参数
        id = request.GET.get('id', '')
        env = request.GET.get('env', '')
        DataView.copy_merchant_id_by_sit1(env_name=env, id=id)
        return Response({'id': id, 'env': env})

    @staticmethod
    def get_modules(env_name):
        sql_dict = Env.objects.filter(envName=env_name)
        return model_to_dict(sql_dict[0])

    # 从sit1 copy
    @staticmethod
    def copy_merchant_id_by_sit1(env_name, id):
        sit1_dict = DataView.get_modules('sit1')
        env_dict = DataView.get_modules(env_name)
        # 查询需要被copy数据
        sit1_connect_dict_all = eval(sit1_dict['sqlDict'])
        # 经销商数据迁移
        sit1_credit_merchant_sign_info = select_mysql('select * from credit_merchant_sign_info where Merchant_ID= "' + id + '";', sit1_connect_dict_all['credittrans'])
        #print(sit1_credit_merchant_sign_info)
        #print(select_mysql('show columns from credit_merchant_sign_info;', sit1_connect_dict_all['credittrans']))
        print(select_mysql('select column_name from information_schema.columns where table_name = "credit_merchant_sign_info";', sit1_connect_dict_all['credittrans']))
        #operate_mysql('INSERT INTO credit_merchant_sign_info')






