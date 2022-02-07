from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django.apps import apps


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'about_me', 'image', 'user')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(User, UserAdmin)

app = apps.get_app_config('graphql_auth')

for model_name, model in app.models.items():
    admin.site.register(model)