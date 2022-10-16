from django.contrib import admin
from .models import User, UserFollower, Post, PostLike

# Register your models here.

admin.site.register(User)
admin.site.register(UserFollower)
admin.site.register(Post)
admin.site.register(PostLike)