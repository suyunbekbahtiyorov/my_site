from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=155)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
