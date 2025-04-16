from django.forms import *
from projects.models import *
from django.contrib.auth import get_user_model


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


class ListForm(ModelForm):
    class Meta:
        model = List
        fields = ['name']

    def save(self):
        list = super().save(commit=False)
        return list


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description']

    def save(self):
        task = super().save(commit=False)
        return task


User = get_user_model()


class AddMemberForm(ModelForm):
    user = ModelChoiceField(
        queryset=User.objects.all(),
        label="Пользователь",
        widget=Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Member
        fields = ['user', 'role']
        widgets = {
            'role': Select(attrs={'class': 'form-select'})
        }
        labels = {
            'role': 'Роль'
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super().__init__(*args, **kwargs)
        if self.project:
            self.fields['user'].queryset = User.objects.exclude(
                id__in=self.project.members.values('user')
            )

    def clean_user(self):
        user = self.cleaned_data['user']
        if Member.objects.filter(project=self.project, user=user).exists():
            raise ValidationError("Этот пользователь уже в проекте")
        return user
