from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from .models import Project, Genre



def index(request):
    projects = Project.objects.order_by('short_name').prefetch_related('genres')
    for project in projects.all():
        url = '/images/covers/' + project.short_name + '/cover01_small.jpg'
        setattr(project, 'cover_url', url)
        print(vars(project));
        print('\n')
    for project in projects.all():
        print(vars(project));
        print('\n')
    context = {
        'projects': projects,
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
    for project in projects:
        project.cover_url: '/images/covers/' + project.short_name + '/cover01_small.jpg'
    context = {
        'projects': projects,
        'title': current_genre.name 
    }
    return render(request, 'projects/index.html', context)
