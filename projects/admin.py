from django.contrib import admin

from .models import  Chapter, Project, Genre, ProjectGenre, Author, Person, Job, Role, Volume, Work, TitleRelate, ProjectsInNeed, Title
from users.models import User

class GenreAdmin(admin.ModelAdmin):
    def titles_counter(self, obj):
        return obj.title_set.count()  
    list_display = ('name', 'genre_type', 'titles_counter')
    list_display_links = None
    list_editable = ('name', 'genre_type')
    list_filter = ['genre_type']
    search_fields = ['name']

class JobAdmin(admin.ModelAdmin):
    def titles_counter(self, obj):
        return obj.title_set.count()  
    list_display = ('name', 'next_job', 'hide')
    list_display_links = None
    list_editable = ('name', 'next_job', 'hide')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_kanji', 'birthplace', 'birthday', 'blood_type', 'twitter')
    list_display_link = ('name')
    list_editable = ('name_kanji', 'birthplace', 'birthday', 'blood_type', 'twitter')
    search_fields = ['name']

class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_kanji', 'type', 'is_hentai', 'total_volumes', 'state_japan')
    list_display_link = ('name')
    list_editable = ('name_kanji', 'type', 'is_hentai', 'total_volumes', 'state_japan')
    list_filter = ('state_japan', 'is_hentai', 'type')
    search_fields = ['name']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter_prefix', 'state', 'text_state')
    list_display_link = ('name')
    list_editable = ('state', 'text_state')
    list_filter = ['state']
    search_fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('person', 'title', 'description', 'work')
    list_display_link = ('person')
    list_editable = ('description', 'work')
    search_fields = ('person', 'title')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('project', 'job', 'user', 'description')
    list_editable = ['description']
    list_filter = ['job']
    search_fields = ('project', 'job', 'user')

class VolumeAdmin(admin.ModelAdmin):
    list_display = ('project', 'order_number', 'number', 'specific_name')
    list_editable = ('order_number', 'number', 'specific_name')
    search_fields = ['project']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ('project', 'number', 'title', 'order_number', 'prefix_title', 'volume', 'active', 'state')
    list_display_link = ['number']
    list_editable = ('title', 'order_number', 'prefix_title', 'active', 'state')
    list_filter = ['state']
    search_fields = ['project']

class RolekAdmin(admin.ModelAdmin):
    list_display = ('project', 'number', 'title', 'order_number', 'prefix_title', 'volume', 'active', 'state')
    list_display_link = ['number']
    list_editable = ('title', 'number', 'order_number', 'prefix_title', 'active', 'state')
    list_filter = ['state']
    search_fields = ['project']

class ProjectGenreAdmin(admin.ModelAdmin):
    list_display = ('project', 'genre')
    list_display_link = ['number']
    list_filter = ['genre']
    search_fields = ['project', 'genre']

class WorkAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'job', 'user', 'prev_work')

class TitleRelateAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_related', 'relation_type')
    list_editable = ['relation_type']
    list_filter = ['relation_type']

class ProjectsInNeedAdmin(admin.ModelAdmin):
    list_display = ('project', 'job', 'job_text', 'description', 'active')
    list_editable = ('job_text', 'description', 'active')

# Register your models here.
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(ProjectGenre, ProjectGenreAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Volume, VolumeAdmin)
admin.site.register(Work, WorkAdmin)
admin.site.register(TitleRelate, TitleRelateAdmin)
admin.site.register(ProjectsInNeed, ProjectsInNeedAdmin)
admin.site.register(Title, TitleAdmin)