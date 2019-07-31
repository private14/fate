import pymysql
from data_migration.views import *
import datetime
from decimal import *
from time import sleep


# 操作 pymysql
def connect_mysql(mysql_dict):
    db = pymysql.connect(
        host=mysql_dict['host'],
        user=mysql_dict['user'],
        password=mysql_dict['password'],
        database=mysql_dict['database'],
        port=int(mysql_dict['port'])
    )
    return db


# 查询
def select_mysql(sql, mysql_dict):
    db = connect_mysql(mysql_dict)
    cursor = db.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    assert data is not None
    if len(list(data)) == 1:
        data = list(list(data)[0])
    else:
        data = list(data)
    cursor.close()
    db.close()
    return data


def select_one_date(sql_data_list, mysql_dict):
    db = connect_mysql(mysql_dict)
    cursor = db.cursor()
    if 'and' in sql_data_list.keys():
        sql = 'select {} from {} where {}="{}" and {};'.format(sql_data_list['*'], sql_data_list['table'],
                                                               sql_data_list['condition'], sql_data_list['value'],
                                                               sql_data_list['and'])
    else:
        sql = 'select {} from {} where {}="{}";'.format(sql_data_list['*'], sql_data_list['table'],
                                                        sql_data_list['condition'], sql_data_list['value'])
    cursor.execute(sql)
    data = cursor.fetchall()
    assert data is not None
    if len(list(data)) == 1:
        data = list(list(data)[0])
    else:
        data = list(data)
    cursor.close()
    db.close()
    return data


# 操作
def operate_mysql(sql, mysql_dict):
    db = connect_mysql(mysql_dict)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()


# 变成可以插入的数据
def insert_data(mysql_data):
    screening = []
    for i in mysql_data:
        if type(i) is datetime.datetime or type(i) is datetime.date:
            screening.append(str(i))
        elif i is None:
            screening.append('None')
        elif type(i) == Decimal:
            screening.append(float(i))
        else:
            screening.append(i)
    screening = str(tuple(screening))
    return screening
