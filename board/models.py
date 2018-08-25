from django.conf import settings
from django.db import models

# Create your models here.

class Post(models.Model):
<<<<<<< HEAD
    name = models.CharField(max_length=150)
=======

>>>>>>> 128cb9ce2249db6650bd3313593772c67f531350
    title = models.CharField(max_length=100, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post',on_delete=models.CASCADE,)
    author = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
