from django.contrib import admin

from .models import  Chapter, Project, Genre, ProjectGenre, Author, Person, Job, Role, Volume, Work, TitleRelate, ProjectsInNeed

# Register your models here.
admin.site.register(Chapter)
admin.site.register(Project)
admin.site.register(Genre)
admin.site.register(ProjectGenre)
admin.site.register(Author)
admin.site.register(Person)
admin.site.register(Job)
admin.site.register(Role)
admin.site.register(Volume)
admin.site.register(Work)
admin.site.register(TitleRelate)
admin.site.register(ProjectsInNeed)