from django.contrib import admin

from .models import PostCategory, PostLike, Post


admin.site.register(PostCategory)
admin.site.register(PostLike)
admin.site.register(Post)
