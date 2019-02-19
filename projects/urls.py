from django.urls import path

from . import views

urlpatterns = [
    path('projects', views.index, name='projects'),
    path('projects/<int:id>/', views.project, name='project')
]
