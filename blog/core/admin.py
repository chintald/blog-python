from django.contrib import admin
from .models import Post, Tag, Comment

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'created_on', 'updated_on')
    list_filter = ('tags', 'created_on', 'updated_on')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)} # this create the slug field from the title field
    autocomplete_fields = ('tags',)

admin.site.register(Post, PostAdmin)

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

admin.site.register(Tag, TagAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'content')

admin.site.register(Comment, CommentAdmin)