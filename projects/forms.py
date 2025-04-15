from django.forms import *
from projects.models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']

    def save(self):
        project = super().save(commit=False)
        return project
