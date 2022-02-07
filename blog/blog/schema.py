import graphene
from graphene_django import DjangoObjectType
from graphql_auth.schema import UserQuery, MeQuery
from core import schema as core_schema
from users import schema as user_schema
from graphql_auth import mutations

#Query

class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    token_auth = mutations.ObtainJSONWebToken.Field()
    update_account = mutations.UpdateAccount.Field()


class Query(MeQuery, core_schema.Query, user_schema.Query, graphene.ObjectType):
    pass
    
class Mutation(AuthMutation, core_schema.Mutation, user_schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)