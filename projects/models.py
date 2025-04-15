from django.db import models
from authentication.models import User


class Member(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=63)
    created_at = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
