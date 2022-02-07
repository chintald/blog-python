from graphql import GraphQLError 


def can(*permissions):
    def wrapped_decorator(func):
        def inner(cls, info, *args, **kwargs):
             
            if not info.context:
                raise GraphQLError("Permission Denied.")
 
            user = info.context.user
            if not user.is_authenticated or not user.role:
                raise GraphQLError("Permission Denied.")
 
            # An admin (Django superusers) can do everything.
            if user.is_superuser:
                return func(cls, info, **kwargs)
 
            # A user CAN perform an action, if he has ANY of the requested permissions.
            user_permissions = list(
                user.get_all_permissions()
            )
 
            if any(permission in user_permissions for permission in permissions):
                return func(cls, info, **kwargs)
            raise GraphQLError("Permission Denied.")
 
        return inner
 
    return wrapped_decorator