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


class Board(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="boards"
    )
    name = models.CharField(max_length=63)
    description = models.TextField()
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_boards"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [["project", "name"]]


class List(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="lists"
    )
    name = models.CharField(max_length=63)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_lists"
    )

    class Meta:
        unique_together = [["board", "name"]]

    created_at = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    list = models.ForeignKey(
        List,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    name = models.CharField(max_length=63)
    description = models.TextField()
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
