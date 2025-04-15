from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from projects.forms import ProjectForm


class CreateProjectView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request):
        return render(request, 'create_project.html', {"form": ProjectForm()})

    @staticmethod
    @login_required(login_url='login')
    def post(request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.owner = request.user
            project.save()
            return redirect('projects')
        return render(request, 'create_project.html', {"form": form})


class ProjectsView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request):
        context = {
            'projects': request.user.project_set.all()
        }
        return render(request, 'projects.html', context)
