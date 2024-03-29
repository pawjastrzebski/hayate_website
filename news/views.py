import random
from django.shortcuts import render
from projects.models import Project, Chapter, Volume, ProjectsInNeed
from .models import News

def index(request):
    ids = Project.no_hentai.values_list('title_id', flat=True)
    ids = list(ids)
    n = 4
    rand_ids = random.sample(ids, n)
    random_projects = Project.objects.filter(title_id__in=rand_ids).prefetch_related('title__genres')
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title').only('title', 'number', 'project__slug', 'project__title__name')
    ids = list(ProjectsInNeed.objects.values_list('id', flat=True))
    n = 2
    rand_ids = random.sample(ids, n)
    projects_in_need = ProjectsInNeed.objects.filter(id__in=rand_ids).select_related('project');

    context = {
        'latests': latests,
        'projects': random_projects,
        'projects_in_need': projects_in_need,
        'title': '',
        'news': News.objects.order_by('date').all().prefetch_related('user')
    }
    return render(request, 'news/index.html', context)
