from email import contentmanager
import email
from urllib import request
import graphene
from graphene_django import DjangoObjectType
from core.models import Tag, Post, Comment
from users. models import User, Profile
from users.schema import UserType
import graphql_jwt
from graphql import GraphQLError

#Schema for Tag Start
class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ("id", "name")
    
class CreateTag(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True )

    tag = graphene.Field(TagType)

    def mutate(self,info, name):
        if info.context.user.is_superuser:
            tag = Tag.objects.create(
                name = name
            )
            tag.save()

        else:
            raise GraphQLError('You must be an admin to create a tag!')

        return CreateTag(
            tag = tag
        )

class UpdateTag(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        id = graphene.ID()

    tag = graphene.Field(TagType)

    def mutate(self, info,id, name=None):
        if info.context.user.is_superuser:
            tag = Tag.objects.get(pk=id)
            tag.name = name if name is not None else tag.name

            tag.save()

        else:
            raise GraphQLError('You must be an admin to update the tag!')

        return UpdateTag(tag=tag)

  #No need of delete tag as the tags are defined by admin

class DeleteTag(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    
    tag = graphene.Field(TagType)

    def mutate(self, info, id):
        if info.context.user.is_superuser:
            tag = Tag.objects.get(pk=id)
            if Tag is not None:
                tag.delete()
        
        else:
            raise GraphQLError('You must be an admin to delete the tag!')
        
        return DeleteTag(tag=tag)

#Schema for Tag End

#Schema for Comment Start

class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ("id", "name", "email", "content", "post", "created")

#### Have doubts regarding Comment mutations

class CreaeteComment(graphene.Mutation):
    class Arguments:
        # name = graphene.String(required=True)
        # email = graphene.String(required=True)
        content = graphene.String(required=True)
        post_id = graphene.ID(required=True)
        

    comment = graphene.Field(CommentType)

    def mutate(self, info, content,post_id):
        post = Post.objects.get(id=post_id)
        if info.context.user.is_superuser or info.context.user.is_authenticated:
            if post is not None:
                comment = Comment.objects.create(
                    name=info.context.user.username,
                    email=info.context.user.email,
                    content=content,
                    post=Post.objects.get(id=post_id)
                )
            comment.save()
        return CreaeteComment(
            comment = comment
        )

class UpdateComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    class Arguments:
        comment_id = graphene.ID(required=True)
        content = graphene.String()

    def mutate(self, info, comment_id, content):
        comment = Comment.objects.get(id=comment_id)
        if info.context.user.is_superuser or info.context.user.username == comment.name:
            comment.content = content
            comment.save()
        else:
            raise GraphQLError('You must be an admin to update comment!')

        return UpdateComment(comment=comment)

class DeleteComment(graphene.Mutation):
    comment = graphene.Field(CommentType)
    class Arguments:
        comment_id = graphene.ID(required=True)
    
    def mutate(self, info, comment_id):
        comment = Comment.objects.get(id=comment_id)
        if info.context.user.is_superuser or info.context.user.username == comment.name:
            comment.delete()
        else:
            raise GraphQLError('You must be an admin to delete the comment!')

        return DeleteComment(comment=comment)
#Schema for Comment End



class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ("id", "title", "slug", "author", "content", "image", "tags", "created_on", "updated_on")

class CreatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        title = graphene.String(required=True)
        slug = graphene.String(required=True)
        content = graphene.String(required=True)

    def mutate(self, info, title, slug, content):
        if info.context.user.is_authenticated:
            post = Post.objects.create(
                title = title,
                slug = slug,
                content = content,
                author = User.objects.get(username=info.context.user.username)
            )

        else:
            raise GraphQLError('Failed to upload post.')

        return CreatePost(post=post)


class UpdatePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.ID(required=True)
        content = graphene.String()
        title = graphene.String()
    
    def mutate(self, info, post_id, content, title):
        post = Post.objects.get(id=post_id)


        if info.context.user.is_superuser or info.context.user.is_authenticated:
            post.content = content
            post.title = title
            
            post.save()

        else:
            raise GraphQLError('You must be an admin to Update the post!')

        return UpdatePost(post=post)

class DeletePost(graphene.Mutation):
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.ID(required=True)

    def mutate(self, info, post_id):
        post = Post.objects.get(id=post_id)
        # post_author = User.objects.get(username=post.author)
        

        
        if info.context.user.is_superuser or info.context.user.is_authenticated:
            post.delete()
        
        else:
            raise GraphQLError('You must be an admin to Delete the post!')

        return DeletePost(post=post)

#Qery for whole schema

class Query(graphene.ObjectType):

    #For Posts

    all_posts = graphene.List(PostType)
    post_title = graphene.Field(PostType, title=graphene.String())
    post_slug = graphene.Field(PostType, slug=graphene.String())
    post_tag = graphene.List(TagType, tag=graphene.String())
    post_author = graphene.Field(UserType, author=graphene.String())
    post_content = graphene.Field(PostType, content=graphene.String())
    post_created_on = graphene.Field(PostType, created_on=graphene.String())
    post_updated_on = graphene.Field(PostType, updated_on=graphene.String())
        
    def resolve_all_posts(root, info):
        return(
            Post.objects.prefetch_related("tags")
            .select_related("author").all()
            )


    def resolve_post_author(root, info, author):
        return(
            User.objects.get(author=author) 
        )

    def resolve_post_slug(root, info, slug):
        return(
            Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )


    def resolve_post_tag(root, info, tag):
        return (
            Tag.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    def resolve_post_content(root, info, content):
        return(
            Post.objects.get(content=content)
        )

    def resolve_post_created_on(root, info, created_on):
        return(
            Post.objects.get(created_on=created_on)
        )

    def resolve_post_updated_on(root, inof, updated_on):
        return(
            Post.objects.get(updated_on=updated_on)
        )
    
    #for comments
    all_comments = graphene.List(CommentType)
    comment_user_name = graphene.Field(CommentType, name=graphene.String())
    comment_user_email = graphene.Field(CommentType, email=graphene.String())
    comment_content = graphene.Field(CommentType, content=graphene.String())
    comment_post_title = graphene.Field(CommentType, post=graphene.String())
    comment_created_on = graphene.Field(CommentType, created=graphene.String())

    def resolve_all_comments(root, info):
        return(
            Comment.objects.all()
        )
        
    def resolve_comment_user_name(root, info, name):
        return(
            Comment.objects.get(name=name)
        )
    
    def resolve_comment_user_email(root, info, email):
        return(
            Comment.objects.get(email=email)
        )

    def resolve_comment_content(root, info, content):
        return(
            Comment.objects.get(content=content)
        )

    def resolve_post_title(root, info, post):
        return(
            Comment.objects.get(post=post)
        )

    def resolve_comment_created_on(root, info, created):
        return(
            Comment.objects.get(creaeted=created)
        )

    #For Tags
    all_tags = graphene.List(TagType)
    tag = graphene.Field(TagType, tag=graphene.String())

    def resolve_all_tags(root, info):
        return(
            Tag.objects.all()
        )
    
        

    def resolve_tag(root, info, tag):
        return(
            Tag.objects.get(tag=tag)
        )


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
    create_tag = CreateTag.Field()
    update_tag = UpdateTag.Field()
    delte_tag = DeleteTag.Field()
    create_comment = CreaeteComment.Field()
    update_comment = UpdateComment.Field()
    delete_comment = DeleteComment.Field()
