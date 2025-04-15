from django.forms import *
from projects.models import *


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def save(self):
        project = super().save(commit=False)
        return project


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ['name', 'description']

    def save(self):
        board = super().save(commit=False)
        return board
