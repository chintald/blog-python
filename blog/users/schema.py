import email
import profile
import graphql_jwt
from shutil import unregister_unpack_format
from xml.dom import UserDataHandler
import graphene
from graphene_django import DjangoObjectType
import users
from users.models import User, Profile
from blog.utils import can 
from graphql_jwt.decorators import login_required
from graphql import GraphQLError
import graphql_jwt

#Schema for User

class UserFields:
    id = graphene.ID()
    username = graphene.String(required=True)
    password = graphene.String(required=True)
    email = graphene.String(required=True)

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "email", "username")


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        
        if info.context.user.is_superuser:
            user = User.objects.create(
                username=username,
                email=email,
            )
            user.set_password(password)
            user.save()
        else:
            raise GraphQLError('You must be an admin to createuser!')
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        id = graphene.Int(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, username, password, email, id):
        user = User.objects.get(pk=id)
        if info.context.user.is_superuser or id == info.context.user.id:
            
            user.username = username
            user.email = email

            user.set_password(password)
            user.save()
        else:
            raise GraphQLError('You must be an admin to Update the user!')

        return UpdateUser(user=user)


## Should not Delete user as it is not a nullable field | and it is an admin task which should be done from an admin panel

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    user = graphene.Field(UserType)

    def mutate(self, info, id):
        if info.context.user.is_superuser:
            user = User.objects.get(pk=id)
            if user is not None:
                user.delete()

        else:
            raise GraphQLError('You must be an admin to Delete the user!')

        return DeleteUser(user=user)


        



class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ("id", "about_me", "image", "user")

class CreateProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        about_me = graphene.String()
        user = graphene.String()
    
    def mutate(self, info, about_me, user):
        if info.context.user.is_superuser:
            profile = Profile.objects.create(
                about_me=about_me,
                user=user
            )

            profile.save()
        else:
            raise GraphQLError('You must be an admin to create this profile!')

        return CreateProfile(profile=profile)

class UpdateProfile(graphene.Mutation):

    class Arguments:
        about_me = graphene.String()
        user = graphene.String()
        user_id = graphene.Int()
        profile_id = graphene.Int()

    profile = graphene.Field(ProfileType)

    def mutate(self, info, about_me, user, profile_id, user_id):
        user = User.objects.get(pk=user_id)
        profile = Profile.objects.get(pk=profile_id)
        if info.context.user.is_superuser or user.id == info.context.user.id:

            profile.about_me = about_me
            profile.user = user

            profile.save()

        else:
            raise GraphQLError('You must be an admin to update this profile!')

        return UpdateProfile(profile=profile)

class DeleteProfile(graphene.Mutation):
    profile = graphene.Field(ProfileType)

    class Arguments:
        profile_id = graphene.Int()

    def mutate(self,info,profile_id):
        if info.context.user.is_superuser:
            profile = Profile.objects.get(pk=profile_id)
            if profile is not None:
                profile.delete()

        else:
            raise GraphQLError('You must be an admin to Delete the Profile!')

        return DeleteProfile(profile=profile)



class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    profile = graphene.List(ProfileType)
    current_user = graphene.Field(UserType)

    @login_required
    def resolve_current_user(self, info):
        if info.context.user.is_superuser:
            return User.objects.all()
        else:
            return info.context.user

    @login_required

    def resolve_users(self, info):
        if info.context.user.is_superuser:
            user = User.objects.all()
        
        else:
            raise GraphQLError('You must be an admin to see the users!')

        return user

    def resolve_profile(self, info):
        if info.context.user.is_superuser:
            profile = Profile.objects.all()
        
        else:
            raise GraphQLError('You must be an admin to see the profiles!')
        
        return profile


#Mutation Class

class Mutation(graphene.ObjectType):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    create_user =  CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    create_profile = CreateProfile.Field()
    update_profile = UpdateProfile.Field()
    delete_profile = DeleteProfile.Field()