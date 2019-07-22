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
