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


# 测试项目
class Project(models.Model):
    # id
    id = models.AutoField(primary_key=True)
    # 项目名字
    projectName = models.CharField(max_length=50)

    class Meta:
        db_table = 'Project'
        ordering = ['id']
