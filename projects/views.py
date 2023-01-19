import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader, RequestContext
from django.db.models import Q, Count, Prefetch
from .models import Project, Genre, Chapter, Volume, Title, Person, Author




def index(request):
    projects = Project.no_hentai.all()
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    context = {
        'latests': latests,
        'projects': projects,
        'title': 'Wszystkie projekty'
    }
    return render(request, 'projects/index.html', context)

def projects_active(request):
    projects = Project.no_hentai.active().all()
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    context = {
        'latests': latests,
        'projects': projects,
        'title': 'Projekty aktywne'
    }
    return render(request, 'projects/index.html', context)

def projects_completed(request):
    projects = Project.no_hentai.completed().all()
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    context = {
        'latests': latests,
        'projects': projects,
        'title': 'Projekty zakończone'
    }
    return render(request, 'projects/index.html', context)

def projects_abandoned(request):
    projects = Project.no_hentai.abandoned().all()
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    context = {
        'latests': latests,
        'projects': projects,
        'title': 'Projekty porzucone'
    }
    return render(request, 'projects/index.html', context)

def projects_licensed(request):
    projects = Project.no_hentai.licensed().all()
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    context = {
        'latests': latests,
        'projects': projects,
        'title': 'Projekty zlicencjonowane'
    }
    return render(request, 'projects/index.html', context)

def project(request, slug_name):
    current_project = Project.single_project
    current_project = current_project.get(slug=slug_name)    
    volumes = Volume.objects.distinct().filter(project__slug = slug_name, chapter__state=1).order_by('order_number').prefetch_related(Prefetch('chapter_set', queryset=Chapter.objects.filter(state=1).order_by('order_number')))
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')

    context = {
        'latests': latests,
        'project': current_project,
        'title':  current_project.title.name,
        'volumes': volumes
    }
    return render(request, 'projects/project.html', context)

def projects_for_genre(request, slug_name):
    projects = Project.no_hentai.filter(title__genres__slug = slug_name).all()
    genre_name = Genre.objects.get(slug = slug_name).name
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')

    context = {
        'projects': projects,
        'title': 'Projekty z tagiem: ' + genre_name.lower(),
        'latests': latests  
    }
    return render(request, 'projects/index.html', context)

def projects_for_person(request, slug_name):
    projects = Project.no_hentai.filter(title__authors__slug = slug_name).all()
    author_name = Person.objects.get(slug = slug_name).name
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')

    context = {
        'projects': projects,
        'title':  'Projekty dla autora: ' + author_name,
        'latests': latests
    }
    return render(request, 'projects/index.html', context)

def download_chapter(request, chapter_id):
    data = [chapter_id, request.META.REMOTE_ADDR, request.META.HTTP_REFFERER]
    with open(os.path.join(settings.BASE_DIR, 'projects/log.txt'), 'a') as log_file:
        log_file.write('\n')
        log_file.write(', '.join(data))

    chapter_file = os.path.join(settings.FILES_DIR, chapter_relative_path)
    chapter_relative_path = Chapter.objects.filter(id=chapter_id).first().filename
    if chapter_relative_path[0] == '/':
        chapter_relative_path = chapter_relative_path[1:]
    chapter_filename = os.path.basename(chapter_relative_path)
    path = os.path.join(settings.FILES_DIR, chapter_relative_path)
    chapter_file = open(path, 'rb')
    response = HttpResponse(content=chapter_file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{chapter_filename}"'
    return response



