from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    #auto_now will update timestamp every time model is saved, so when user edits post it will refresh the post to the top of the feed chronologically
    timestamp = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")