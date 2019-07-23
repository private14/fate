from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views import View
from accounts.models import *
from django.forms.models import model_to_dict
from common_function.operate_sql import *
import json
import datetime


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
    def copy_merchant_id_by_sit1(env_name, id, source='sit1'):
        sit1_dict = DataView.get_modules(source)
        env_dict = DataView.get_modules(env_name)
        # 查询需要被copy sql 链接信息
        sit1_connect_dict_all = eval(sit1_dict['sqlDict'])
        env_connect_dict_all = eval(env_dict['sqlDict'])
        ### credittrans ###
        # 表 credit_merchant_sign_info 商品平台签约信息
        sit1_credit_merchant_sign_info = select_mysql(
            'select * from credit_merchant_sign_info where Merchant_ID= "{}";'.format(id),
            sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_sign_info != []:
            sql_data_list = {
                '*': 'merchant_sign_id',
                'table': 'credit_merchant_sign_info',
                'condition': 'merchant_id',
                'value': str(id)
            }
            sit1_merchant_sign_id = select_one_date(sql_data_list, sit1_connect_dict_all['credittrans'])
            sql_data_list = {
                '*': '*',
                'table': 'credit_merchant_sign_info',
                'condition': 'merchant_sign_id',
                'value': str(sit1_merchant_sign_id[0])
            }
            if select_one_date(sql_data_list, env_connect_dict_all['credittrans'])!= []:
                # 删除
                operate_mysql('delete from credit_merchant_sign_info where {}="{}"'.format('merchant_sign_id', sit1_merchant_sign_id[0]),env_connect_dict_all['credittrans'])
            operate_mysql('INSERT INTO credit_merchant_sign_info VALUES {};'.format(insert_data(sit1_credit_merchant_sign_info).replace("'None'", "Null")), env_connect_dict_all['credittrans'])
        # 表 credit_merchant_sign_product_info 商户签约列表
        sit1_credit_merchant_sign_product_info = select_mysql('select * from credit_merchant_sign_product_info where Merchant_ID= "{}";'.format(id), sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_sign_product_info != []:
            sql_data_list = {
                '*': 'sign_id',
                'table': 'credit_merchant_sign_product_info',
                'condition': 'merchant_id',
                'value': str(id)
            }
            sit1_sign_id = select_one_date(sql_data_list, sit1_connect_dict_all['credittrans'])
            sql_data_list = {
                '*': '*',
                'table': 'credit_merchant_sign_product_info',
                'condition': 'sign_id',
                'value': str(sit1_sign_id[0])
            }
            if select_one_date(sql_data_list, env_connect_dict_all['credittrans']) != []:
                # 删除
                operate_mysql('delete from credit_merchant_sign_product_info where {}="{}"'.format('sign_id', sit1_sign_id[0]), env_connect_dict_all['credittrans'])
            operate_mysql('INSERT INTO credit_merchant_sign_product_info VALUES {};'.format(insert_data(sit1_credit_merchant_sign_product_info).replace("'None'", "Null")), env_connect_dict_all['credittrans'])
        # 表 credit_merchant_review_serial 商户审批流水
        sit1_credit_merchant_review_serial = select_mysql('select * from credit_merchant_review_serial where Merchant_ID= "{}";'.format(id), sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_review_serial != []:
            sql_data_list = {
                '*': 'apply_id',
                'table': 'credit_merchant_review_serial',
                'condition': 'merchant_id',
                'value': str(id)
            }
            sit1_apply_id = select_one_date(sql_data_list, sit1_connect_dict_all['credittrans'])
            sql_data_list = {
                '*': '*',
                'table': 'credit_merchant_review_serial',
                'condition': 'apply_id',
                'value': str(sit1_apply_id[0])
            }
            if select_one_date(sql_data_list, env_connect_dict_all['credittrans']) != []:
                # 删除
                operate_mysql('delete from credit_merchant_review_serial where {}="{}"'.format('apply_id', sit1_apply_id[0]),
                              env_connect_dict_all['credittrans'])
            operate_mysql('INSERT INTO credit_merchant_review_serial VALUES {};'.format(
                insert_data(sit1_credit_merchant_review_serial).replace("'None'", "Null")), env_connect_dict_all['credittrans'])
        # 表 credit_merchant_product_limit_info 商户产品贷款额度信息表
        sit1_credit_merchant_product_limit_info = select_mysql(
            'select * from credit_merchant_product_limit_info where Merchant_ID= "{}";'.format(id),
            sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_product_limit_info != []:
            sql_data_list = {
                '*': '*',
                'table': 'credit_merchant_review_serial',
                'condition': 'merchant_id',
                'value': str(id)
            }
            if select_one_date(sql_data_list, env_connect_dict_all['credittrans']) != []:
                # 删除
                operate_mysql(
                    'delete from credit_merchant_product_limit_info where {}="{}"'.format('merchant_id', str(id)),
                    env_connect_dict_all['credittrans'])
            operate_mysql('INSERT INTO credit_merchant_product_limit_info VALUES {};'.format(
                insert_data(sit1_credit_merchant_product_limit_info).replace("'None'", "Null")),
                env_connect_dict_all['credittrans'])
        # 表 credit_merchant_limit_info 商户贷款额度信息表
        sit1_credit_merchant_limit_info = select_mysql('select * from credit_merchant_limit_info where Merchant_ID= "{}";'.format(id), sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_limit_info != []:
            sql_data_list = {
                '*': '*',
                'table': 'credit_merchant_limit_info',
                'condition': 'merchant_id',
                'value': str(id)
            }
            print('INSERT INTO credit_merchant_limit_info VALUES {};'.format(insert_data(sit1_credit_merchant_limit_info).replace("'None'", "Null")))
            if select_one_date(sql_data_list, env_connect_dict_all['credittrans']) != []:
                # 删除
                operate_mysql('delete from credit_merchant_limit_info where {}="{}"'.format('merchant_id', str(id)), env_connect_dict_all['credittrans'])
            operate_mysql('INSERT INTO credit_merchant_limit_info VALUES {};'.format(insert_data(sit1_credit_merchant_limit_info).replace("'None'", "Null")), env_connect_dict_all['credittrans'])
