from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='projects'),
    path('<int:id>/', views.project, name='project'),
    path('genre/<int:id>/', views.projectsForGenre, name='projectsForGenre')
]
