from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


# Create your models here.

class CustomUser(AbstractUser):
    """
    Custom user model with added phoneNumber field.
    """
    groups = models.ManyToManyField(Group,related_name="custom_user_groups",blank=True)
    user_permissions = models.ManyToManyField(Permission,related_name="custom_user_permissions", blank=True)
    phoneNumber = models.CharField(max_length=10)


class Question(models.Model): 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    title = models.CharField(max_length=255) 
    created_at = models.DateTimeField(auto_now_add=True)


class Answer(models.Model): 
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers') 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 
    likes = models.ManyToManyField(CustomUser, related_name='liked_answers', blank=True)