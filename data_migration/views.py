from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views import View
from accounts.models import *
from django.forms.models import model_to_dict
from common_function.operate_sql import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json
import datetime


class DataView(APIView):
    """
    get:
        Return a highlight instance
    """
    @api_view(['GET'])
    def copy_merchant_id(request):
        # 获取传入参数
        id = request.GET.get('id', '')
        env = request.GET.get('env', '')
        source = request.GET.get('source', '')
        return Response(DataView.copy_merchant_id_by_sit1(env_name=env, id=id, source=source))

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
        # 表 credit_merchant_sign_product_info 商户签约列表
        sit1_credit_merchant_sign_product_info = select_mysql('select * from credit_merchant_sign_product_info where {}="{}" and status = "01";'.format('product_id', id), sit1_connect_dict_all['credittrans'])
        if select_mysql('select merchant_id from credit_merchant_sign_product_info where {}="{}" and status = "01";'.format('product_id', id), sit1_connect_dict_all['credittrans']) == []:
            return "merchant_id 未关联到产品id 请关联后尝试"
        else:
            merchant_id = str(select_mysql(
                'select merchant_id from credit_merchant_sign_product_info where {}="{}" and status = "01";'.format(
                    'product_id', id), sit1_connect_dict_all['credittrans'])[0])
        sign_id = select_mysql('select sign_id from credit_merchant_sign_product_info where {}="{}" and status = "01";'.format('product_id', id), sit1_connect_dict_all['credittrans'])
        if sign_id != []:
            for i in sign_id:
                operate_mysql('delete from credit_merchant_sign_product_info where {}="{}"'.format('sign_id', i), env_connect_dict_all['credittrans'])
                operate_mysql('INSERT INTO credit_merchant_sign_product_info VALUES {};'.format(insert_data(sit1_credit_merchant_sign_product_info).replace("'None'", "Null")), env_connect_dict_all['credittrans'])
        # 表 credit_merchant_sign_info 商品平台签约信息
        sit1_credit_merchant_sign_info = select_mysql('select * from credit_merchant_sign_info where Merchant_ID= "{}";'.format(merchant_id),sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_sign_info != []:
            sql_data_list = {
                '*': 'merchant_sign_id',
                'table': 'credit_merchant_sign_info',
                'condition': 'merchant_id',
                'value': merchant_id
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
        # 表 credit_merchant_review_serial 商户审批流水
        sit1_credit_merchant_review_serial = select_mysql('select * from credit_merchant_review_serial where Merchant_ID= "{}";'.format(merchant_id), sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_review_serial != []:
            sql_data_list = {
                '*': 'apply_id',
                'table': 'credit_merchant_review_serial',
                'condition': 'merchant_id',
                'value': merchant_id
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
            'select * from credit_merchant_product_limit_info where Merchant_ID= "{}";'.format(merchant_id),
            sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_product_limit_info != []:
            sql_data_list = {
                '*': '*',
                'table': 'credit_merchant_review_serial',
                'condition': 'merchant_id',
                'value': merchant_id
            }
            if select_one_date(sql_data_list, env_connect_dict_all['credittrans']) != []:
                # 删除
                operate_mysql(
                    'delete from credit_merchant_product_limit_info where {}="{}"'.format('merchant_id', merchant_id),
                    env_connect_dict_all['credittrans'])

            if type(sit1_credit_merchant_product_limit_info[0]) == str:
                operate_mysql('INSERT INTO credit_merchant_product_limit_info VALUES {};'.format(
                    insert_data(sit1_credit_merchant_product_limit_info).replace("'None'", "Null")),
                    env_connect_dict_all['credittrans'])
            else:
                for i in sit1_credit_merchant_product_limit_info:
                    operate_mysql('INSERT INTO credit_merchant_product_limit_info VALUES {};'.format(insert_data(i).replace("'None'", "Null")), env_connect_dict_all['credittrans'])
                    # 表 credit_merchant_limit_info 商户贷款额度信息表
        sit1_credit_merchant_limit_info = select_mysql('select * from credit_merchant_limit_info where Merchant_ID= "{}";'.format(merchant_id), sit1_connect_dict_all['credittrans'])
        if sit1_credit_merchant_limit_info != []:
            sql_data_list = {
                '*': '*',
                'table': 'credit_merchant_limit_info',
                'condition': 'merchant_id',
                'value': merchant_id
            }
            if select_one_date(sql_data_list, env_connect_dict_all['credittrans']) != []:
                # 删除
                operate_mysql('delete from credit_merchant_limit_info where {}="{}"'.format('merchant_id', merchant_id), env_connect_dict_all['credittrans'])
            operate_mysql('INSERT INTO credit_merchant_limit_info VALUES {};'.format(insert_data(sit1_credit_merchant_limit_info).replace("'None'", "Null")), env_connect_dict_all['credittrans'])
        ### Product ###
        # 表 product_product 产品
        sit1_product_product = select_mysql('select * from product_product where {}="{}";'.format('product_id', id), sit1_connect_dict_all['product'])
        if sit1_product_product != []:
            sql_data_list = {
                '*': '*',
                'table': 'product_product',
                'condition': 'product_id',
                'value': id
            }
            if select_one_date(sql_data_list, env_connect_dict_all['product']) != []:
                # 删除
                operate_mysql('delete from product_product where {}="{}"'.format('product_id', id), env_connect_dict_all['product'])
            operate_mysql('INSERT INTO product_product VALUES {};'.format(insert_data(sit1_product_product).replace("'None'", "Null")), env_connect_dict_all['product'])
        # 表 product_product_resource 产品资源关系
        sit1_product_product_resource = select_mysql('select * from product_product_resource where {}="{}";'.format('product_id', id), sit1_connect_dict_all['product'])
        if sit1_product_product != []:
            sql_data_list = {
                '*': '*',
                'table': 'product_product_resource',
                'condition': 'product_id',
                'value': id
            }
            if select_one_date(sql_data_list, env_connect_dict_all['product']) != []:
                # 删除
                operate_mysql('delete from product_product_resource where {}="{}"'.format('product_id', id),
                              env_connect_dict_all['product'])
            if len(sit1_product_product_resource[0]) >= 2:
                for i in sit1_product_product_resource:
                    operate_mysql('INSERT INTO product_product_resource VALUES {};'.format(insert_data(i).replace("'None'", "Null")), env_connect_dict_all['product'])
            else:
                operate_mysql('INSERT INTO product_product_resource VALUES {};'.format(
                        insert_data(sit1_product_product_resource).replace("'None'", "Null")), env_connect_dict_all['product'])
        # 表 product_product_param_group 产品属性组
        sit1_product_product_param_group = select_mysql('select * from product_product_param_group where {}="{}";'.format('product_id', id), sit1_connect_dict_all['product'])
        if sit1_product_product_param_group != []:
            sql_data_list = {
                '*': '*',
                'table': 'product_product_param_group',
                'condition': 'product_id',
                'value': id
            }
            if select_one_date(sql_data_list, env_connect_dict_all['product']) != []:
                # 删除
                operate_mysql('delete from product_product_param_group where {}="{}"'.format('product_id', id),
                              env_connect_dict_all['product'])
            if len(sit1_product_product_param_group[0]) >= 2:
                for i in sit1_product_product_param_group:
                    operate_mysql('INSERT INTO product_product_param_group VALUES {};'.format(insert_data(i).replace("'None'", "Null")), env_connect_dict_all['product'])
            else:
                operate_mysql('INSERT INTO product_product_param_group VALUES {};'.format(
                        insert_data(sit1_product_product_param_group).replace("'None'", "Null")), env_connect_dict_all['product'])
        # 表 product_product_param 产品属性
        sit1_product_product_param = select_mysql('select * from product_product_param where {}="{}";'.format('product_id', id), sit1_connect_dict_all['product'])
        if sit1_product_product_param != []:
            sql_data_list = {
                '*': '*',
                'table': 'product_product_param_group',
                'condition': 'product_id',
                'value': id
            }
            if select_one_date(sql_data_list, env_connect_dict_all['product']) != []:
                # 删除
                operate_mysql('delete from product_product_param where {}="{}"'.format('product_id', id),
                              env_connect_dict_all['product'])
            if len(sit1_product_product_param[0]) >= 2:
                for i in sit1_product_product_param:
                    operate_mysql('INSERT INTO product_product_param VALUES {};'.format(insert_data(i).replace("'None'", "Null")), env_connect_dict_all['product'])
            else:
                operate_mysql('INSERT INTO product_product_param VALUES {};'.format(
                        insert_data(sit1_product_product_param).replace("'None'", "Null")), env_connect_dict_all['product'])
        # 表 product_interest_rule 息费规则表
        sql_data_list = {
            '*': 'resource_id',
            'table': 'product_product_resource',
            'condition': 'product_id',
            'value': id,
            'and': 'resource_type=1'
        }
        if select_one_date(sql_data_list, sit1_connect_dict_all['product']) != []:
            resource_id_rule = select_one_date(sql_data_list, sit1_connect_dict_all['product'])
            for i in resource_id_rule:
                if select_mysql('select * from product_interest_rule where {}="{}"'.format('interest_rule_id', i[0]), env_connect_dict_all['product']) != []:
                    operate_mysql('delete from product_interest_rule where {}="{}"'.format('interest_rule_id', i[0]), env_connect_dict_all['product'])
                operate_mysql('INSERT INTO product_interest_rule VALUES {};'.format(insert_data(select_mysql('select * from product_interest_rule where {}="{}";'.format('interest_rule_id', i[0]), sit1_connect_dict_all['product']))).replace("'None'", "Null"), env_connect_dict_all['product'])
        # 表 product_interest_price_param 息费定价属性表
        if resource_id_rule != []:
            for i in resource_id_rule:
                if select_mysql('select * from product_interest_price_param where {}="{}"'.format('INTEREST_RULE_ID', i[0]), env_connect_dict_all['product']) != []:
                    operate_mysql('delete from product_interest_price_param where {}="{}"'.format('INTEREST_RULE_ID', i[0]), env_connect_dict_all['product'])
                a = select_mysql('select * from product_interest_price_param where {}="{}";'.format('interest_rule_id', i[0]), sit1_connect_dict_all['product'])
                for y in a:
                    operate_mysql('INSERT INTO product_interest_price_param VALUES {};'.format(y), env_connect_dict_all['product'])
        # 表 product_contract 合同
        sql_data_list = {
            '*': 'resource_id',
            'table': 'product_product_resource',
            'condition': 'product_id',
            'value': id,
            'and': 'resource_type=3'
        }
        # 之后的操作
        if select_one_date(sql_data_list, sit1_connect_dict_all['product']) != []:
            compact_id = select_one_date(sql_data_list, sit1_connect_dict_all['product'])
            for i in compact_id:
                # 删除 contract_id
                contract_id = select_mysql(
                    'select contract_id from product_contract where {}="{}"'.format('compact_id', i),
                    sit1_connect_dict_all['product'])
                for x in contract_id:
                    operate_mysql('delete from product_contract where {}="{}"'.format('contract_id', x[0]), env_connect_dict_all['product'])
                # 删除 compact_id
                if select_mysql('select * from product_contract where {}="{}"'.format('compact_id', i), env_connect_dict_all['product']) != []:
                    operate_mysql(
                        'delete from product_contract where {}="{}"'.format('compact_id', i),
                        env_connect_dict_all['product'])
                a = select_mysql(
                    'select * from product_contract where {}="{}";'.format('compact_id', i),
                    sit1_connect_dict_all['product'])
                for y in a:
                    operate_mysql('INSERT INTO product_contract VALUES {};'.format(insert_data(y).replace("'None'", "Null")),
                                  env_connect_dict_all['product'])
        # 表 product_contract_param
        sql_data_list = {
            '*': 'resource_id',
            'table': 'product_product_resource',
            'condition': 'product_id',
            'value': id,
            'and': 'resource_type=3'
        }
        trade_param = select_mysql('select trade_param from product_biz_serial;', sit1_connect_dict_all['product'])
        # 之后的操作
        if select_one_date(sql_data_list, sit1_connect_dict_all['product']) != []:
            compact_id = select_one_date(sql_data_list, sit1_connect_dict_all['product'])
            for i in compact_id:
                contract_id = select_mysql(
                    'select contract_id from product_contract where {}="{}"'.format('compact_id', i),
                    sit1_connect_dict_all['product'])
                for x in contract_id:
                    operate_mysql(
                        'delete from product_contract_param where {}="{}"'.format('contract_id', x[0]), env_connect_dict_all['product'])
                for x in contract_id:
                    operate_mysql('INSERT INTO product_contract_param VALUES {};'.format(insert_data(select_mysql('select * from product_contract_param where {}="{}"'.format('contract_id', x[0]), sit1_connect_dict_all['product'])).replace("'None'", "Null")), env_connect_dict_all['product'])

                    # 表 product_contract_participant 合同参与者
                    relate_id = select_mysql('select relate_id from product_contract_participant where {}="{}"'.format('contract_id', x[0]), sit1_connect_dict_all['product'])
                    # 删除 relate_id
                    operate_mysql('delete from product_contract_participant where {}="{}"'.format('relate_id', relate_id[0]), env_connect_dict_all['product'])
                for x in contract_id:
                    operate_mysql('INSERT INTO product_contract_participant VALUES {};'.format(insert_data(select_mysql('select * from product_contract_participant where {}="{}"'.format('relate_id', relate_id[0]), sit1_connect_dict_all['product'])).replace("'None'", "Null")), env_connect_dict_all['product'])

                    # 表 product_biz_serial 合同参与者
                    participant_id = select_mysql('select participant_id from product_contract_participant where {}="{}"'.format('contract_id', x[0]), sit1_connect_dict_all['product'])
                    for z in trade_param:
                        if participant_id[0] in str(z):
                            serial_id = select_mysql("select serial_id from product_biz_serial where {}='{}';".format('trade_param', str(z[0])), sit1_connect_dict_all['product'])
                            operate_mysql('delete from product_biz_serial where {}="{}"'.format('serial_id', serial_id[0]), env_connect_dict_all['product'])
                            operate_mysql('INSERT INTO product_biz_serial VALUES {};'.format(insert_data(select_mysql('select * from product_biz_serial where {}="{}"'.format('serial_id', serial_id[0]), sit1_connect_dict_all['product'])).replace("'None'", "Null")),env_connect_dict_all['product'])

        # 表 product_compact 合约表
        sql_data_list = {
            '*': 'resource_id',
            'table': 'product_product_resource',
            'condition': 'product_id',
            'value': id,
            'and': 'resource_type=3'
        }
        if select_one_date(sql_data_list, sit1_connect_dict_all['product']) != []:
            resource_id = select_one_date(sql_data_list, sit1_connect_dict_all['product'])
            for i in resource_id:
                operate_mysql('delete from product_compact where {}="{}"'.format('compact_id', i[0]), env_connect_dict_all['product'])
            for i in resource_id:
                operate_mysql('INSERT INTO product_compact VALUES {};'.format(insert_data(select_mysql('select * from product_compact where {}="{}"'.format('compact_id', i[0]), sit1_connect_dict_all['product'])).replace("'None'", "Null")), env_connect_dict_all['product'])

                # 表 product_compact_param 合约属性表
                param_id = select_mysql('select param_id from product_compact_param where {}="{}";'.format('compact_id', i[0]), sit1_connect_dict_all['product'])
                for y in param_id:
                    operate_mysql('delete from product_compact_param where {}="{}"'.format('param_id', y[0]), env_connect_dict_all['product'])
                for y in param_id:
                    operate_mysql('INSERT INTO product_compact_param VALUES {};'.format(insert_data(
                        select_mysql('select * from product_compact_param where {}="{}"'.format('param_id', y[0]),
                                     sit1_connect_dict_all['product'])).replace("'None'", "Null")), env_connect_dict_all['product'])

        ### asset ###
        if merchant_id != []:
            # 表 asset_cash_deposit_info 商户平台签约信息
            if select_mysql('select * from asset_cash_deposit_info where {}="{}";'.format('partner_user_id', merchant_id), sit1_connect_dict_all['asset']) != []:
                operate_mysql('delete from asset_cash_deposit_info where {}="{}"'.format('partner_user_id', merchant_id), env_connect_dict_all['asset'])
                operate_mysql('INSERT INTO asset_cash_deposit_info VALUES {};'.format(insert_data(select_mysql('select * from asset_cash_deposit_info where {}="{}"'.format('partner_user_id', merchant_id), sit1_connect_dict_all['asset'])).replace("'None'", "Null")), env_connect_dict_all['asset'])
            # 表 asset_quota_info 指标信息表
            asset_quota_info = select_mysql('select * from asset_quota_info where {}="{}";'.format('partner_user_id', merchant_id), sit1_connect_dict_all['asset'])
            if asset_quota_info != []:
                operate_mysql('delete from asset_quota_info where {}="{}"'.format('partner_user_id', merchant_id),
                              env_connect_dict_all['asset'])
                for i in asset_quota_info:
                    operate_mysql('INSERT INTO asset_quota_info VALUES {};'.format(insert_data(i)).replace("'None'", "Null"), env_connect_dict_all['asset'])
            # 表 asset_quota_serial 指标信息表变更流水表
            operate_mysql('delete from asset_quota_serial where {}="{}"'.format('partner_user_id', merchant_id),
                          env_connect_dict_all['asset'])
            operate_mysql('INSERT INTO asset_quota_serial VALUES {};'.format(insert_data(select_mysql(
                'select * from asset_quota_serial where {}="{}"'.format('partner_user_id', merchant_id),
                sit1_connect_dict_all['asset'])).replace("'None'", "Null")), env_connect_dict_all['asset'])

        ### loanuser ###
        if merchant_id != []:
            # 表 user_customer_relation 客户与客户关系
            if select_mysql('select * from user_customer_relation where {}="{}";'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser']) != []:
                operate_mysql('delete from user_customer_relation where {}="{}"'.format('user_id', merchant_id),
                              env_connect_dict_all['loanuser'])
                operate_mysql('INSERT INTO user_customer_relation VALUES {};'.format(insert_data(select_mysql(
                    'select * from user_customer_relation where {}="{}"'.format('user_id', merchant_id),
                    sit1_connect_dict_all['loanuser'])).replace("'None'", "Null")), env_connect_dict_all['loanuser'])
            # 表 user_customer_resource_relation 客户资源项关系表
            resource_id_user = select_mysql('select resource_id from user_customer_resource_relation where {}="{}";'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser'])
            for i in resource_id_user:
                operate_mysql('delete from user_customer_resource_relation where {}="{}"'.format('resource_id', i[0]),
                              env_connect_dict_all['loanuser'])
                if select_mysql('select * from user_customer_resource_relation where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                    operate_mysql('INSERT INTO user_customer_resource_relation VALUES {};'.format(insert_data(select_mysql('select * from user_customer_resource_relation where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser'])).replace("'None'", "Null")), env_connect_dict_all['loanuser'])
            # 表 user_financial_instruments_info 金融工具表
            for i in resource_id_user:
                operate_mysql('delete from user_financial_instruments_info where {}="{}"'.format('resource_id', i[0]),
                              env_connect_dict_all['loanuser'])
                if select_mysql('select * from user_financial_instruments_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                    operate_mysql('INSERT INTO user_financial_instruments_info VALUES {};'.format(insert_data(select_mysql('select * from user_financial_instruments_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser'])).replace("'None'", "Null")), env_connect_dict_all['loanuser'])
            # 表 user_image_data_info 影像资料表
            for i in resource_id_user:
                operate_mysql('delete from user_image_data_info where {}="{}"'.format('resource_id', i[0]),
                              env_connect_dict_all['loanuser'])
                if select_mysql('select * from user_image_data_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                    operate_mysql('INSERT INTO user_image_data_info VALUES {};'.format(insert_data(select_mysql('select * from user_image_data_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser'])).replace("'None'", "Null")), env_connect_dict_all['loanuser'])
            # 表 user_organ_basic_info 机构基本信息表
            user_organ_basic_info = select_mysql('select * from user_organ_basic_info where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser'])
            if user_organ_basic_info != []:
                operate_mysql('delete from user_organ_basic_info where {}="{}"'.format('user_id', merchant_id), env_connect_dict_all['loanuser'])
                operate_mysql('INSERT INTO user_organ_basic_info VALUES {};'.format(insert_data(user_organ_basic_info).replace("'None'", "Null")), env_connect_dict_all['loanuser'])
            # 表 user_resource_index 资源项索引表
            indexes_id = []
            for i in resource_id_user:
                indexes_id.append(select_mysql('select indexes_id from user_resource_index where {}="{}";'.format('resource_id', i), sit1_connect_dict_all['loanuser']))
            for y in indexes_id:
                if y != []:
                    operate_mysql('delete from user_resource_index where {}="{}"'.format('indexes_id', y),
                                  env_connect_dict_all['loanuser'])
                    operate_mysql('INSERT INTO user_resource_index VALUES {};'.format(
                        insert_data(insert_data(select_mysql('select * from user_resource_index where {}="{}"'.format('indexes_id', y), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null")), env_connect_dict_all['loanuser'])
            # 表 user_resource_info 资源项信息表
            for i in resource_id_user:
                operate_mysql('delete from user_resource_info where {}="{}"'.format('resource_id', i[0]), env_connect_dict_all['loanuser'])
                if select_mysql('select * from user_resource_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser']):
                    operate_mysql('INSERT INTO user_resource_info VALUES {};'.format(insert_data(select_mysql('select * from user_resource_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # 表 user_role_resource_relation 角色资源项关系表
            for i in resource_id_user:
                operate_mysql('delete from user_role_resource_relation where {}="{}"'.format('resource_id', i[0]),
                              env_connect_dict_all['loanuser'])
                if select_mysql('select * from user_role_resource_relation where {}="{}"'.format('resource_id', i[0]),
                                sit1_connect_dict_all['loanuser']):
                    operate_mysql('INSERT INTO user_role_resource_relation VALUES {};'.format(insert_data(
                        select_mysql('select * from user_role_resource_relation where {}="{}"'.format('resource_id', i[0]),
                                     sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"),
                                  env_connect_dict_all['loanuser'])
            # 表 user_contact_station_info 联系点表
            station_id = select_mysql('select station_id from user_contact_station_info where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser'])
            cust_role_id = select_mysql(
                'select cust_role_id from user_contact_station_info where {}="{}"'.format('user_id', merchant_id),
                sit1_connect_dict_all['loanuser'])
            if station_id != []:
                for i in station_id:
                    operate_mysql('delete from user_contact_station_info where {}="{}"'.format('station_id', i[0]),
                              env_connect_dict_all['loanuser'])
                    operate_mysql('INSERT INTO user_contact_station_info VALUES {};'.format(insert_data(
                        select_mysql('select * from user_contact_station_info where {}="{}"'.format('station_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # 表 user_customer_role_relation 客户角色表
            if cust_role_id != []:
                for i in cust_role_id:
                    operate_mysql('delete from user_customer_role_relation where {}="{}"'.format('cust_role_id', i[0]), env_connect_dict_all['loanuser'])
                    if select_mysql('select * from user_customer_role_relation where {}="{}"'.format('cust_role_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                        operate_mysql('INSERT INTO user_customer_role_relation VALUES {};'.format(insert_data(select_mysql('select * from user_customer_role_relation where {}="{}"'.format('cust_role_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # 表 user_tel_contact_station_info 电话联系点
            if station_id != []:
                for i in station_id:
                    operate_mysql('delete from user_tel_contact_station_info where {}="{}"'.format('station_id', i[0]),
                                  env_connect_dict_all['loanuser'])
                    if select_mysql('select * from user_tel_contact_station_info where {}="{}"'.format('station_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                        operate_mysql('INSERT INTO user_tel_contact_station_info VALUES {};'.format(insert_data(select_mysql('select * from user_tel_contact_station_info where {}="{}"'.format('station_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])

            # 表 user_personal_basic_info 个人客户基本信息表
            operate_mysql('delete from user_personal_basic_info where {}="{}"'.format('user_id', merchant_id), env_connect_dict_all['loanuser'])
            if select_mysql('select * from user_personal_basic_info where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser']) != []:
                operate_mysql('INSERT INTO user_personal_basic_info VALUES {};'.format(insert_data(select_mysql('select * from user_personal_basic_info where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # 表 user_identify 识别表
            auth_id = select_mysql('select auth_id from user_customer_role_relation where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser'])
            if auth_id != [None]:
                identify_id = []
                for i in auth_id:
                    identify_id.append(select_mysql('select * from user_identify where {}="{}"'.format('auth_id', i[0]), sit1_connect_dict_all['loanuser']))
                for y in identify_id:
                    operate_mysql('delete from user_identify where {}="{}"'.format('identify_id', y[0]), env_connect_dict_all['loanuser'])
                    if select_mysql('select * from user_identify where {}="{}"'.format('identify_id', y[0]), sit1_connect_dict_all['loanuser']) != []:
                        operate_mysql('INSERT INTO user_identify VALUES {};'.format(insert_data(select_mysql('select * from user_identify where {}="{}"'.format('identify_id', y[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # 表 user_leaguer_info 会员表
            leaguer_id = select_mysql('select leaguer_id from user_leaguer_info where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser'])
            for i in leaguer_id:
                operate_mysql('delete from user_leaguer_info where {}="{}"'.format('leaguer_id', i[0]), env_connect_dict_all['loanuser'])
                if select_mysql('select * from user_leaguer_info where {}="{}"'.format('leaguer_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                    operate_mysql('INSERT INTO user_leaguer_info VALUES {};'.format(insert_data(select_mysql('select * from user_leaguer_info where {}="{}"'.format('leaguer_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # user_customer_info 客户信息表
            operate_mysql('delete from user_customer_info where {}="{}"'.format('user_id', merchant_id), env_connect_dict_all['loanuser'])
            if select_mysql('select * from user_customer_info where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser']) != []:
                operate_mysql('INSERT INTO user_customer_info VALUES {};'.format(insert_data(
                    select_mysql('select * from user_customer_info where {}="{}"'.format('user_id', merchant_id),
                                 sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"),
                              env_connect_dict_all['loanuser'])
            # user_auth_id 通行证表
            for i in auth_id:
                if i != None:
                    operate_mysql('delete from user_auth_id where {}="{}"'.format('auth_id', i[0]), env_connect_dict_all['loanuser'])
                    if select_mysql('select * from user_auth_id where {}="{}"'.format('auth_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                        operate_mysql('INSERT INTO user_auth_id VALUES {};'.format(insert_data(select_mysql('select * from user_auth_id where {}="{}"'.format('auth_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # user_auth_id_symbol 通行证识别表
            for i in auth_id:
                if i != None:
                    symbol_id = select_mysql('select symbol_id from user_auth_id_symbol where {}="{}"'.format('auth_id', i[0]), sit1_connect_dict_all['loanuser'])
                    for y in symbol_id:
                        operate_mysql('delete from user_auth_id_symbol where {}="{}"'.format('symbol_id', y[0]), env_connect_dict_all['loanuser'])
                        if select_mysql('select * from user_auth_id_symbol where {}="{}"'.format('symbol_id', y[0]), sit1_connect_dict_all['loanuser']) != []:
                            operate_mysql('INSERT INTO user_auth_id_symbol VALUES {};'.format(insert_data(select_mysql('select * from user_auth_id_symbol where {}="{}"'.format('symbol_id', y[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"),env_connect_dict_all['loanuser'])
            # 表 user_certificate_info 证件文档表
            for i in resource_id_user:
                if i != None:
                    operate_mysql('delete from user_certificate_info where {}="{}"'.format('resource_id', i[0]), env_connect_dict_all['loanuser'])
                    if select_mysql('select * from user_certificate_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                        operate_mysql('INSERT INTO user_certificate_info VALUES {};'.format(insert_data(select_mysql('select * from user_certificate_info where {}="{}"'.format('resource_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # 表 user_address_contact_station_info 地址联系点
            for i in station_id:
                if i != None:
                    operate_mysql('delete from user_address_contact_station_info where {}="{}"'.format('station_id', i[0]), env_connect_dict_all['loanuser'])
                    if select_mysql('select * from user_address_contact_station_info where {}="{}"'.format('station_id', i[0]), sit1_connect_dict_all['loanuser']) != []:
                        operate_mysql('INSERT INTO user_address_contact_station_info VALUES {};'.format(insert_data(select_mysql('select * from user_address_contact_station_info where {}="{}"'.format('station_id', i[0]), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])
            # 表 user_organization_info 组织表
            creator = select_mysql('select creator from user_organ_basic_info where {}="{}"'.format('user_id', merchant_id), sit1_connect_dict_all['loanuser'])
            if creator != None:
                organ_id = select_mysql('select organ_id from user_organization_info where {}="{}"'.format('creator', creator), sit1_connect_dict_all['loanuser'])
                if organ_id != None:
                    operate_mysql('delete from user_organization_info where {}="{}"'.format('organ_id', organ_id), env_connect_dict_all['loanuser'])
                    if select_mysql('select * from user_organization_info where {}="{}"'.format('organ_id', organ_id), sit1_connect_dict_all['loanuser']) != []:
                        operate_mysql('INSERT INTO user_organization_info VALUES {};'.format(insert_data(select_mysql('select * from user_organization_info where {}="{}"'.format('organ_id', organ_id), sit1_connect_dict_all['loanuser']))).replace("'None'", "Null"), env_connect_dict_all['loanuser'])

        return 'pass'

