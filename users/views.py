from django.shortcuts import render
from .models import User
from projects.models import Chapter

# Create your views here.

def index(request):
    members = User.objects.filter(active = 1)
    retired_members = User.objects.filter(active = 0, pk__gte='1')
    latests = Chapter.objects.filter(project__title__is_hentai = 0, state = 1).all().order_by('-date', '-order_number')[:15].select_related('project', 'project__title', 'volume').only('title', 'volume', 'number', 'project__slug', 'project__title__name')
    context = {
        'latests': latests,
        'members': members,
        'retired_members': retired_members,
        'title': 'Hayateńczycy'
    }
    return render(request, 'users/members.html', context)