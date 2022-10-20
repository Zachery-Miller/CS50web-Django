from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=280, verbose_name="Content")
    time_posted = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize_post(self, liked_by_active_user):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "time_posted": self.time_posted.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes,
            "liked_by_active_user": liked_by_active_user
        }

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked")

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")