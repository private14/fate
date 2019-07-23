import graphene
from graphene_django.types import DjangoObjectType
from accounts.models import *


class UserType(DjangoObjectType):
    class Meta:
        model = User


# 定义动作，类似POST, PUT, DELETE
class UserInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    account = graphene.String(required=True)
    password = graphene.String(required=True)
    level = graphene.String()
    emails = graphene.String(required=True)
    name = graphene.String(required=True)


# 定义一个创建user的mutation
class CreateUser(graphene.Mutation):
    # api的输入参数
    class Arguments:
        user_data = UserInput(required=True)

    # api的响应参数
    ok = graphene.Boolean()
    user = graphene.Field(UserType)

    # api的相应操作，这里是create
    def mutate(self, info, user_data):
        user = User.objects.create(id=user_data['id'], account=user_data['account'], password=user_data['password'], level=user_data['level'], emails=user_data['emails'], name=user_data['name'])
        ok = True
        return CreateUser(user=user, ok=ok)


# 定义查询，类似GET
class Query(object):
    all_user = graphene.List(UserType)
    
    def resolve_all_user(self, info, **kwargs):
        # 查询所有book的逻辑
        return User.objects.all()
