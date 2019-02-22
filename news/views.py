import random
from django.shortcuts import render
from projects.models import Project, Chapter, Volume
from .models import News

def index(request):
    ids = Project.objects.filter(age_limit__lte=17).values_list('id', flat=True)
    ids = list(ids)
    n = 4
    rand_ids = random.sample(ids, n)
    random_projects = Project.objects.filter(id__in=rand_ids).prefetch_related('genres')
    latests = Chapter.objects.all().order_by('-id')[:20].prefetch_related('project')

    context = {
        'latests': latests,
        'projects': random_projects,
        'title': 'Projekty',
        'news': News.objects.order_by('date').all().prefetch_related('user')
    }
    return render(request, 'news/index.html', context)
