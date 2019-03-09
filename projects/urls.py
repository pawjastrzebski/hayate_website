from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='projects'),
    path('aktywne/', views.projects_active, name='projects_active'),
    path('zakonczone/', views.projects_completed, name='projects_completed'),
    path('porzucone/', views.projects_abandoned, name='projects_abandoned'),
    path('zlicencjonowane/', views.projects_licensed, name='projects_licensed'),
    path('<slug:slug_name>/', views.project, name='project'),
    path('genre/<slug:slug_name>/', views.projects_for_genre, name='projects_for_genre'),
    path('person/<slug:slug_name>/', views.projects_for_person, name='projects_for_person'),

]
