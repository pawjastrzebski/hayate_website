import random
from django.shortcuts import render
from projects.models import Project, Chapter, Volume, ProjectsInNeed
from .models import News

def index(request):
    ids = Project.objects.filter(title__is_hentai=0).values_list('title_id', flat=True)
    ids = list(ids)
    n = 4
    rand_ids = random.sample(ids, n)
    random_projects = Project.objects.filter(title_id__in=rand_ids).prefetch_related('title__genres')
    latests = Chapter.objects.filter(project__title__is_hentai = 0, active = 1).all().order_by('-date')[:20].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    projects_in_need = ProjectsInNeed.objects.select_related('project');

    context = {
        'latests': latests,
        'projects': random_projects,
        'projects_in_need': projects_in_need,
        'title': 'Projekty',
        'news': News.objects.order_by('date').all().prefetch_related('user')
    }
    return render(request, 'news/index.html', context)
