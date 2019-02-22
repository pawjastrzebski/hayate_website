import random
from django.shortcuts import render
from projects.models import Project
from .models import News

def index(request):
    ids = Project.objects.values_list('id', flat=True)
    ids = list(ids)
    n = 4
    rand_ids = random.sample(ids, n)
    random_projects = Project.objects.filter(id__in=rand_ids).prefetch_related('genres')

    context = {
        'projects': random_projects,
        'title': 'Projekty',
        "news": News.objects.order_by('date').all().values()
    }
    return render(request, 'news/index.html', context)
