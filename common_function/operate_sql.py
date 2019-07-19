import pymysql
from data_migration.views import *


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


# 复制数据
def copy_data(sql, mysql_dict, copy_to_mysql_dict):
    # 经销商数据迁移
    resource_credit_merchant_sign_info = select_mysql(sql=sql, mysql_dict=mysql_dict)
    print(select_mysql(
        'select column_name from information_schema.columns where table_name = "credit_merchant_sign_info";',
        sit1_connect_dict_all['credittrans']))
    # operate_mysql('INSERT INTO credit_merchant_sign_info')



db = connect_mysql(mysql_dict)
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()