import random
import re
import base64
import requests
# 导入某个模块的部分类或方法
from datetime import *
# 导入常量并重命名
import resource_all.constant as const
from time import sleep
import paramiko
import os
import json


# 创造手机号
def create_phone():
    i = "185"
    while len(i) <= 10:
        i = i + str(random.randint(0, 9))
    return str(i)


# 创造卡号
def create_bank_card():
    i = "620516"
    while len(i) <= 18:
        i = i + str(random.randint(0, 9))
    return str(i)


# 创造人名
def create_name():
    name = random.choice(get_name_list())
    name_len = str(random.randint(1, 2))
    for i in range(int(name_len)):
        name = name + random.choice(get_name_list('firstName'))
    return str(name)


# 获得名字数据
# name参数 lastName or first_name
def get_name_list(name='lastName'):
    with open(os.path.dirname(os.path.realpath(__file__)) + "/people_name.json", 'r') as file:
        load_dict = json.load(file)
    return load_dict[name]


# 创造smsCode
def create_sms_code():
    i = ""
    while len(i) <= 5:
        i = i + str(random.randint(0, 9))
    return str(i)


class IdNumber(str):

    def __init__(self, id_number):
        super(IdNumber, self).__init__()
        self.id = id_number
        self.area_id = int(self.id[0:6])
        self.birth_year = int(self.id[6:10])
        self.birth_month = int(self.id[10:12])
        self.birth_day = int(self.id[12:14])

    def get_area_name(self):
        """根据区域编号取出区域名称"""
        return const.AREA_INFO[self.area_id]

    def get_birthday(self):
        """通过身份证号获取出生日期"""
        return "{0}-{1}-{2}".format(self.birth_year, self.birth_month, self.birth_day)

    def get_age(self):
        """通过身份证号获取年龄"""
        now = (datetime.now() + timedelta(days=1))
        year, month, day = now.year, now.month, now.day

        if year == self.birth_year:
            return 0
        else:
            if self.birth_month > month or (self.birth_month == month and self.birth_day > day):
                return year - self.birth_year - 1
            else:
                return year - self.birth_year

    def get_sex(self):
        """通过身份证号获取性别， 女生：0，男生：1"""
        return int(self.id[16:17]) % 2

    def get_check_digit(self):
        """通过身份证号获取校验码"""
        check_sum = 0
        for i in range(0, 17):
            check_sum += ((1 << (17 - i)) % 11) * int(self.id[i])
        check_digit = (12 - (check_sum % 11)) % 11
        return check_digit if check_digit < 10 else 'X'

    @classmethod
    def verify_id(cls, id_number):
        """校验身份证是否正确"""
        if re.match(const.ID_NUMBER_18_REGEX, id_number):
            check_digit = cls(id_number).get_check_digit()
            return str(check_digit) == id_number[-1]
        else:
            return bool(re.match(const.ID_NUMBER_15_REGEX, id_number))

    @classmethod
    def generate_id(cls, sex=1):
        """随机生成身份证号，sex = 0表示女性，sex = 1表示男性"""

        # 随机生成一个区域码(6位数)
        id_number = str(random.choice(list(const.AREA_INFO.keys())))
        # 限定出生日期范围(8位数)
        start, end = datetime.strptime("1960-01-01", "%Y-%m-%d"), datetime.strptime("2000-12-30", "%Y-%m-%d")
        birth_days = datetime.strftime(start + timedelta(random.randint(0, (end - start).days + 1)), "%Y%m%d")
        id_number += str(birth_days)
        # 顺序码(2位数)
        id_number += str(random.randint(10, 99))
        # 性别码(1位数)
        id_number += str(random.randrange(sex, 10, step=2))
        # 校验码(1位数)
        return id_number + str(cls(id_number).get_check_digit())


def create_random_number(number):
    i = ""
    while len(i) <= number-1:
        i = i + str(random.randint(0, 9))
    return str(i)


def create_photo_base64(photo_path):
    with open(photo_path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
        s = base64_data.decode()
    return s


# 身份证
def create_identity_card(risk_control='on'):
    if risk_control == 'on':
        i = "31042819930102" + str(random.randint(0, 9))
        while len(i) <= 17:
            i = i + str(random.randint(0, 9))
        return i
    elif risk_control == 'off':
        return IdNumber.generate_id().upper()
    else:
        print('构建身份证参数传入错误 风控开关只能on or off')
        assert 1 > 2, '构建身份证参数传入错误 风控开关只能on or off'


# sftp 下载
def sftp_download():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("192.168.10.207", 22, "kaka", "kaka@sftp123")

