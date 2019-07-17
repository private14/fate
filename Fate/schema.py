import graphene
import accounts.schema


class Query(accounts.schema.Query, graphene.ObjectType):
    # 总的Schema的query入口
    pass


class Mutations(graphene.ObjectType):
    # 总的Schema的mutations入口
    create_user = accounts.schema.CreateUser.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
