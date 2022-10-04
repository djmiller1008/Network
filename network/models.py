from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

class UserFollowers(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="folowee")
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers") 
    



