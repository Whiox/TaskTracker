from django.urls import path
from projects.views import *

urlpatterns = [
    path('create', CreateProjectView.as_view(), name='create_project'),
    path('', ProjectsView.as_view(), name='projects'),
]
