<<<<<<< HEAD
# Create your models here.
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    # 其他字段


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # 其他字段
=======
from django.db import models

# Create your models here.
>>>>>>> origin/master
