from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from django.db.models import Q, Count, Prefetch
from .models import Project, Genre, Chapter, Volume, Title, Person



def index(request):
    projects = Project.objects.filter(title__is_hentai = 0, state__gte=1, chapter__state=1).order_by('name').prefetch_related('title__genres', 'title__authors').annotate(number_of_chapters=Count('chapter__id'))
    latests = Chapter.objects.filter(project__title__is_hentai = 0, active = 1).all().order_by('-date')[:20].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    context = {
        'latests': latests,
        'projects': projects,
        'title': 'Projekty'
    }
    return render(request, 'projects/index.html', context)


def project(request, slug_name):
    current_project = Project.objects.select_related('title').prefetch_related('title__genres', 'title__authors')
    current_project = current_project.get(slug=slug_name)    
    volumes = Volume.objects.filter(project__slug = slug_name).prefetch_related(Prefetch('chapter_set', queryset=Chapter.objects.filter(state=1)))
    latests = Chapter.objects.filter(project__title__is_hentai = 0, active = 1).all().order_by('-date')[:20].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')

    context = {
        'latests': latests,
        'project': current_project,
        'title':  current_project.name,
        'volumes': volumes
    }
    return render(request, 'projects/project.html', context)

def projects_for_genre(request, slug_name):
    current_genre = Genre.objects.get(slug=slug_name)
    projects = current_genre.title_set.order_by('name').prefetch_related('project')
    context = {
        'projects': projects,
        'title': current_genre.name 
    }
    return render(request, 'projects/index.html', context)

def projects_for_person(request, slug_name):
    current_author = Person.objects.get(slug=slug_name)
    projects = current_author.title_set.order_by('name').prefetch_related('project')
    context = {
        'projects': projects,
        'title': current_author.name 
    }
    return render(request, 'projects/index.html', context)
