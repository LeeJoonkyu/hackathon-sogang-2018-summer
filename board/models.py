from django.conf import settings
from django.db import models

# Create your models here.

class Post(models.Model):

    name = models.CharField(max_length=150)
    title = models.CharField(max_length=100, verbose_name='주소를 입력하세요')
    content = models.TextField(verbose_name='계좌번호와 희망 요금을 입력하세요')
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