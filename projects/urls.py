from django.urls import path
from projects.views import *

urlpatterns = [
    path('create', CreateProjectView.as_view(), name='create_project'),
    path('all', ProjectsView.as_view(), name='projects'),
    path('<int:project_id>', ProjectView.as_view(), name='project'),
    path('<int:project_id>/boards/create', CreateBoardView.as_view(), name='create_board'),
]
