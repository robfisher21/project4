from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass


class Posts (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    post = models.CharField(max_length=1000, blank = False, null = False)
    datetime = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name="likes", blank = True, null = True)
    likecount = models.CharField(default=0, max_length=1000, blank = False, null = False)


    class Meta:
        ordering = ['datetime']

    def __str__(self):
        return f"{self.user} : ({self.post})"



class Profile (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="followerlist", blank = True, null = True)
    following = models.ManyToManyField(User, related_name="following", blank = True, null = True)



    class Meta:
        ordering = ['user']
    
    def __str__(self):
        return f"{self.user}'s Profile'"




