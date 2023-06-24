from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "followers": [follow.user.username for follow in self.followers.all()],
            "following": [follow.user.username for follow in self.following.all()],
            "follower_count": self.followers.count(),
            "following_count": self.following.count()
        }

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("User", blank=True, related_name="liked_posts")

    def __str__(self):
        return f"{self.user} posted {self.content} on {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": [user.id for user in self.likes.all()],
            "like_count": self.likes.count()
        }
    
class Follows(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} follows {self.following}"
    
    def serialize(self):
        return {
            "user": self.user.username,
            "following": self.following.username
        }
    
