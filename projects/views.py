from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from projects.forms import *
from projects.models import *


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
            Member.objects.create(
                project=project,
                user=request.user,
                role=Member.Role.ADMIN
            )
            return redirect('projects')
        return render(request, 'create_project.html', {"form": form})


class ProjectsView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request):
        context = {
            'projects': request.user.projects.all()
        }
        return render(request, 'all_projects.html', context)


class ProjectView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request, project_id):
        project = get_object_or_404(Project, id=project_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        context = {
            'project': project,
            'is_owner': is_owner,
            'members': project.members.select_related('user'),
            'boards': project.boards.all()
        }

        return render(request, 'project.html', context)


class CreateBoardView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request, project_id):
        project = get_object_or_404(Project, id=project_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        context = {
            'project': project,
            'form': BoardForm(),
        }

        return render(request, 'create_board.html', context)

    @staticmethod
    @login_required(login_url='login')
    def post(request, project_id):
        project = get_object_or_404(Project, id=project_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save()
            board.project = project
            board.creator = request.user
            board.save()

            return redirect('project', project_id=project_id)

        context = {
            'project': project,
            'form': form
        }

        return render(request, 'create_board.html', context)
