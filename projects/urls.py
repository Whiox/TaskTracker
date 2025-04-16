from django.urls import path
from projects.views import *

urlpatterns = [
    path('create', CreateProjectView.as_view(), name='create_project'),
    path('all', ProjectsView.as_view(), name='projects'),
    path('<int:project_id>', ProjectView.as_view(), name='project'),
    path('<int:project_id>/boards/', BoardsView.as_view(), name='boards'),
    path('<int:project_id>/boards/create', CreateBoardView.as_view(), name='create_board'),
    path('<int:project_id>/boards/<int:board_id>', BoardView.as_view(), name='board'),
    path('<int:project_id>/boards/<int:board_id>/lists/create', CreateListView.as_view(), name='create_list'),
    path('<int:project_id>/boards/<int:board_id>/lists/<int:list_id>/tasks/create',
         CreateTaskView.as_view(), name='create_task'),
    path('tasks/<int:task_id>/move/',
         TaskMoveView.as_view(),
         name='move_task'),
    path(
        'projects/<int:project_id>/add_member/',
        AddMemberView.as_view(),
        name='add_member'
    ),
]
