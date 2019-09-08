from django.contrib import admin

from .models import  Chapter, Project, Genre, ProjectGenre, Author, Person, Job, Role, Volume, Work, TitleRelate, ProjectsInNeed, Title
from users.models import User

class ChapterInline(admin.TabularInline):
    '''Stacked Inline View for Chapter'''
    model = Chapter
    min_num = 1
    max_num = 20

class VolumeInline(admin.TabularInline):
    '''Stacked Inline View for Volume'''
    model = Volume
    min_num = 1
    max_num = 20

class GenreAdmin(admin.ModelAdmin):
    def titles_counter(self, obj):
        return obj.title_set.count()  
    list_display = ('name', 'genre_type', 'titles_counter')
    list_display_links = None
    #list_editable = ('name', 'genre_type')
    list_filter = ['genre_type']
    search_fields = ['name']

class JobAdmin(admin.ModelAdmin):
    def titles_counter(self, obj):
        return obj.title_set.count()  
    list_display = ('name', 'next_job', 'hide')
    list_display_links = None
    #list_editable = ('name', 'next_job', 'hide')

class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_kanji', 'birthplace', 'birthday', 'blood_type', 'twitter')
    list_display_link = ('name')
    #list_editable = ('name_kanji', 'birthplace', 'birthday', 'blood_type', 'twitter')
    search_fields = ['name']

class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_kanji', 'type', 'is_hentai', 'total_volumes', 'state_japan')
    list_display_link = ('name')
    #list_editable = ('name_kanji', 'type', 'is_hentai', 'total_volumes', 'state_japan')
    list_filter = ('state_japan', 'is_hentai', 'type')
    search_fields = ['name']

class ProjectAdmin(admin.ModelAdmin):
    inlines = [VolumeInline]
    list_display = ('name', 'chapter_prefix', 'state', 'text_state')
    list_display_link = ('name')
    #list_editable = ('state', 'text_state')
    list_filter = ['state']
    list_select_related = ['title']
    search_fields = ['name']

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('person', 'title', 'description', 'work')
    list_display_link = ('person')
    #list_editable = ('description', 'work')
    search_fields = ('person', 'title')

class RoleAdmin(admin.ModelAdmin):
    list_display = ('project', 'job', 'user', 'description')
    #list_editable = ['description']
    list_filter = ['job']
    search_fields = ('project', 'job', 'user')

class VolumeAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]
    list_display = ('project', 'order_number', 'number', 'specific_name')
    search_fields = ['project']

class ChapterAdmin(admin.ModelAdmin):
    save_on_top = True;
    list_display = ('project', 'number', 'title', 'order_number', 'prefix_title', 'volume', 'active', 'state')
    list_display_links = ['number']
    list_filter = ['state']
    list_select_related = ('project', 'project__title', 'volume')
    search_fields = ['number', 'project__name']

class ProjectGenreAdmin(admin.ModelAdmin):
    list_display = ('project', 'genre')
    list_display_link = ['number']
    list_filter = ['genre']
    search_fields = ['project', 'genre']

class WorkAdmin(admin.ModelAdmin):
    model = Work
    def get_queryset(self, request):
        return super(WorkAdmin, self).get_queryset(request).select_related(
                'chapter', 'chapter__project', 'chapter__project__title', 'job', 'user').only(
                    'chapter__number', 'chapter__project__title__name', 'job__name', 'user__name', 'date')
    list_display = ('chapter', 'job', 'user', 'date')
    #list_editable = ['date']
    autocomplete_fields = ['chapter']
    fields = ('chapter', 'job', 'user', 'date')
    

class TitleRelateAdmin(admin.ModelAdmin):
    list_display = ('title', 'title_related', 'relation_type')
    #list_editable = ['relation_type']
    list_filter = ['relation_type']

class ProjectsInNeedAdmin(admin.ModelAdmin):
    list_display = ('project', 'job', 'job_text', 'description', 'active')
    #list_editable = ('job_text', 'description', 'active')

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