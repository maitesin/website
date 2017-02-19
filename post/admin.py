from django.contrib import admin

from post.models import Tag, Post, Category, PostTag

admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostTag)
