from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
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
        user = request.user

        owned_projects = user.projects.all()
        member_projects = Project.objects.filter(members__user=user)

        all_projects = (owned_projects | member_projects).distinct()

        context = {
            'projects': all_projects
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


class BoardsView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request, project_id):
        project = get_object_or_404(
            Project.objects.prefetch_related('boards__lists'),
            id=project_id
        )

        if not (request.user == project.owner or
                project.members.filter(user=request.user).exists()):
            return redirect('projects')

        context = {
            'project': project,
            'boards': project.boards.all().order_by('-created_at'),
        }
        return render(request, 'boards.html', context)


class BoardView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request, project_id, board_id):
        project = get_object_or_404(Project, id=project_id)
        board = get_object_or_404(Board, id=board_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        context = {
            'project': project,
            'board': board,
            'lists': board.lists.all(),
            'tasks': board.tasks.all()
        }

        return render(request, 'boards.html', context)


class CreateListView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request, project_id, board_id):
        project = get_object_or_404(Project, id=project_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        context = {
            'project': project,
            'board': get_object_or_404(Board, id=board_id),
            'form': ListForm(),
        }

        return render(request, 'create_list.html', context)

    @staticmethod
    @login_required(login_url='login')
    def post(request, project_id, board_id):
        project = get_object_or_404(Project, id=project_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        form = ListForm(request.POST)
        if form.is_valid():
            list = form.save()
            list.project = project
            list.board = get_object_or_404(Board, id=board_id)
            list.creator = request.user
            list.save()

            return redirect('board', project_id=project_id, board_id=board_id)

        context = {
            'project': project,
            'board': get_object_or_404(Board, id=board_id),
            'form': form
        }

        return render(request, 'create_list.html', context)


class CreateTaskView(View):
    @staticmethod
    @login_required(login_url='login')
    def get(request, project_id, board_id, list_id):
        project = get_object_or_404(Project, id=project_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        context = {
            'project': project,
            'board': get_object_or_404(Board, id=board_id),
            'list': get_object_or_404(List, id=list_id),
            'form': TaskForm()
        }

        return render(request, 'create_task.html', context)

    @staticmethod
    @login_required(login_url='login')
    def post(request, project_id, board_id, list_id):
        project = get_object_or_404(Project, id=project_id)

        is_owner = request.user == project.owner
        is_member = project.members.filter(user=request.user).exists()

        if not (is_owner or is_member):
            return redirect('projects')

        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            task.project = project
            task.board = get_object_or_404(Board, id=board_id)
            task.list = get_object_or_404(List, id=list_id)
            task.creator = request.user
            task.save()

            return redirect('board', project_id=project_id, board_id=board_id)

        context = {
            'project': project,
            'board': get_object_or_404(Board, id=board_id),
            'form': form
        }

        return render(request, 'create_task.html', context)


class TaskMoveView(View):
    @method_decorator(login_required(login_url='login'))
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, task_id):
        try:
            task = Task.objects.select_related(
                'project',
                'board',
                'list'
            ).get(id=task_id)

            is_owner = request.user == task.project.owner
            is_member = task.project.members.filter(user=request.user).exists()

            if not (is_owner or is_member):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Доступ запрещен'
                }, status=403)

            new_list_id = request.POST.get('new_list_id')
            new_list = List.objects.get(id=new_list_id)

            task.list = new_list
            task.order = new_list.tasks.count()
            task.save()

            return JsonResponse({'status': 'success'})

        except Task.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Задача не найдена'
            }, status=404)

        except List.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Лист не найден'
            }, status=404)

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)


class AddMemberView(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        # Проверка прав
        if not (request.user == project.owner or
                project.members.filter(user=request.user, role=Member.Role.ADMIN).exists()):
            return redirect('project', project_id=project_id)

        form = AddMemberForm(project=project)
        return render(request, 'add_member.html', {
            'form': form,
            'project': project
        })

    def post(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)

        # Проверка прав
        if not (request.user == project.owner or
                project.members.filter(user=request.user, role=Member.Role.ADMIN).exists()):
            return redirect('project', project_id=project_id)

        form = AddMemberForm(request.POST, project=project)
        if form.is_valid():
            member = form.save(commit=False)
            member.project = project
            member.save()
            return redirect('project', project_id=project_id)

        return render(request, 'add_member.html', {
            'form': form,
            'project': project
        })
