from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from .models import Project, Genre



def index(request):
    context = {
        'projects': Project.objects.order_by('short_name').prefetch_related('genres'),
        'title': 'Projekty'
    }
    return render(request, 'projects/index.html', context)


def project(request, id):
    current_project = Project.objects.get(pk=id)
    context = {
        'genres': current_project.genres.all().values(),
        'project': current_project,
        'title':  current_project.name
    }
    return render(request, 'projects/project.html', context)

def projectsForGenre(request, id):
    current_genre = Genre.objects.get(pk=id)
    projects = current_genre.project_set.order_by('short_name').prefetch_related('genres')
    context = {
        'projects': projects,
        'title': current_genre.name 
    }
    return render(request, 'projects/index.html', context)
