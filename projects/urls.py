from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='projects'),
    path('<slug:slug_name>/', views.project, name='project'),
    path('genre/<slug:slug_name>/', views.projects_for_genre, name='projects_for_genre'),
    path('person/<slug:slug_name>/', views.projects_for_person, name='projects_for_person'),
    # path('active/', views.projects_active, name='projects_active'),
    # path('completed/', views.projects_completed, name='projects_completed'),
    # path('suspended/', views.projects_suspended, name='projects_suspended'),
    # path('licensed/', views.projects_licensed, name='projects_licensed')
]
