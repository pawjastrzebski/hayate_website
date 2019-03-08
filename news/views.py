import random
from django.shortcuts import render
from projects.models import Project, Chapter, Volume
from .models import News

def index(request):
    ids = Project.objects.filter(title__is_hentai=0).values_list('title_id', flat=True)
    ids = list(ids)
    n = 4
    rand_ids = random.sample(ids, n)
    random_projects = Project.objects.filter(title_id__in=rand_ids).prefetch_related('title__genres')
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date')[:20].prefetch_related('project')

    context = {
        'latests': latests,
        'projects': random_projects,
        'title': 'Projekty',
        'news': News.objects.order_by('date').all().prefetch_related('user')
    }
    return render(request, 'news/index.html', context)
