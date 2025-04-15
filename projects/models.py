from django.db import models
from authentication.models import User

class Project(models.Model):
    name = models.CharField(max_length=63)
    description = models.TextField()
    status = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)

class Member(models.Model):
    class Meta:
        unique_together = [["project", "user"]]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="members"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="project_memberships"
    )

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Администратор"
        DEVELOPER = "DEVELOPER", "Разработчик"
        VIEWER = "VIEWER", "Наблюдатель"

    role = models.CharField(
        max_length=63,
        choices=Role.choices,
        default=Role.VIEWER
    )

    created_at = models.DateTimeField(auto_now_add=True)
