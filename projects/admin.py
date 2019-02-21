from django.contrib import admin

from .models import  Chapter, Project, Genre, ProjectGenre

# Register your models here.
admin.site.register(Chapter)
admin.site.register(Project)
admin.site.register(Genre)
admin.site.register(ProjectGenre)