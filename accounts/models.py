from django.db import models


# 用户信息
class User(models.Model):
    # id
    id = models.AutoField(primary_key=True)
    # 账号
    account = models.CharField(max_length=30)
    # 密码
    password = models.CharField(max_length=30)
    # 级别(权限）
    level = models.CharField(max_length=30, choices=((0, '最高权限'), (1, '可读不可写权限'), (2, '不可读不可写权限')), default=0)
    # email
    emails = models.EmailField(max_length=50, blank=True, null=True)
    # 名字
    name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'User'
        ordering = ['id']


# 测试用例
class TestCase(models.Model):
    # id
    id = models.AutoField(primary_key=True)
    # 测试用例名字
    testCaseName = models.CharField(max_length=500)
    # 测试用例描述
    testCaseDescribe = models.CharField(max_length=500, blank=True, null=True)
    # 初始步骤
    beginSteps = models.CharField(max_length=1000, blank=True, null=True)
    # 步骤
    steps = models.CharField(max_length=2000, blank=True, null=True)
    # 结束步骤
    endSteps = models.CharField(max_length=500, blank=True, null=True)
    # 拥有者
    owner = models.CharField(max_length=10)
    # 是否为公用
    showToAll = models.BooleanField(default=True)
    # 项目
    projectId = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        db_table = 'TestCase'
        ordering = ['id']


# 测试环境
class Env(models.Model):
    # id
    id = models.AutoField(primary_key=True)
    # 环境名字
    envName = models.CharField(max_length=50)
    # 环境url dict
    urlDict = models.CharField(max_length=1000, blank=True, null=True)
    # 环境对应数据库 dict
    sqlDict = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        db_table = 'Env'
        ordering = ['id']


# copy的产品
class CopyProduct(models.Model):
    # id
    id = models.AutoField(primary_key=True)
    # 环境名字
    productId = models.CharField(max_length=50)
    # 环境url dict
    proEnv = models.CharField(max_length=30, blank=True, null=True)
    # 环境对应数据库 dict
    endEnv = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        db_table = 'CopyProduct'
        ordering = ['id']


# 使用过的手机号 名字
class RandomList(models.Model):
    # id
    id = models.AutoField(primary_key=True)
    # 名字
    name = models.CharField(max_length=50)
    # 手机号
    telNumber = models.CharField(max_length=30)
    # 身份证号
    identityCard = models.CharField(max_length=30)
    # 银行卡号
    bankCard = models.CharField(max_length=30)

    class Meta:
        db_table = 'RandomList'
        ordering = ['id']
