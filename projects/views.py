from django.http import HttpResponse
from django.shortcuts import render
from .models import Projects


def index(request):
    context = {
        'projects': Projects.objects.order_by('long_name').values(),
        'title': 'Projekty'
    }
    return render(request, 'projects/index.html', context)


def project(request, id):
    context = {

        'projects': Projects.objects.filter(id=id).values()
    }
    return render(request, 'projects/project.html', context)
