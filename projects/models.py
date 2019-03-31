from django.db import models
from users.models import User
from autoslug import AutoSlugField
from django.urls import reverse
from django.db.models import Count


class NonHentaiQuerySet(models.QuerySet):
    def active(self):
        return self.filter(state=1)
    def completed(self):
        return self.filter(state=2)
    def abandoned(self):
        return self.filter(state=3)
    def licensed(self):
        return self.filter(state=4)   
class NonHentaiProjectsManager(models.Manager):
    def get_queryset(self):
        return NonHentaiQuerySet(self.model, using=self._db).filter(chapter__state=1, state__gte=1, title__is_hentai=0).order_by('name').prefetch_related('title__genres', 'title__authors').annotate(number_of_chapters=Count('chapter__id'))
    def active(self):
        return self.get_queryset().active()
    def completed(self):
        return self.get_queryset().completed()
    def abandoned(self):
        return self.get_queryset().abandoned()
    def licensed(self):
        return self.get_queryset().licensed()

class SingleProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('title').prefetch_related('title__genres', 'title__authors')
    

class Genre(models.Model):
    GENRE_TYPES = (
        (0, "gatunek"),
        (1, "grupa demograficzna"),
        (2, "czasy"),
        (3, "miejsce"),
        (4, "inne")
    )
    id = models.AutoField(primary_key=True)
    genre_type = models.PositiveIntegerField(blank=True, null=True, choices=GENRE_TYPES)
    name = models.CharField(max_length=40, blank=True, null=True)
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='name')

    class Meta:
        db_table = 'genres'
    def get_absolute_url(self):
         return reverse('projects_for_genre', kwargs={'slug_name': self.slug})
    def __str__(self):
        return self.name
    

class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    hide = models.IntegerField()

    class Meta:
        db_table = 'jobs'
    def __str__(self):
        return self.name

class Person(models.Model):
    BLOOD_TYPES = (
        ('0', "0"),
        ('A', "A"),
        ('B', "B"),
        ('AB', "AB")
    )   
    name = models.CharField(unique=True, max_length=100)
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='name')
    name_kanji = models.CharField(unique=True, max_length=255, blank=True,null=True)
    birthplace = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    blood_type = models.CharField(max_length=2, blank=True, null=True, choices=BLOOD_TYPES)
    description = models.TextField(blank=True, null=True)
    twitter = models.CharField(blank=True, null=True, max_length=200)

    class Meta:
        db_table = 'people'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('projects_for_person', kwargs={'slug_name': self.slug})

class Title(models.Model):
    STATES_JAPAN = (
        (0, 'Powstaje'),
        (1, 'Zakończona')
    )
    TYPES_LIST = (
        (0, 'manga'),
        (1, 'anime'),
        (2, 'gra'),
        (3, 'light novel')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(blank=True, null=True, max_length=255)
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='name')
    name_pl = models.CharField(blank=True, null=True, max_length=255)
    name_en = models.CharField(blank=True, null=True, max_length=255)
    name_kanji = models.CharField(blank=True, null=True, max_length=255)
    alternative_names = models.CharField(blank=True, null=True, max_length=255)
    type = models.IntegerField(choices=TYPES_LIST)
    is_hentai = models.IntegerField()
    authors = models.ManyToManyField(Person, through='Author')
    description = models.TextField()
    total_volumes = models.SmallIntegerField()
    state_japan = models.IntegerField(choices=STATES_JAPAN)
    genres = models.ManyToManyField(Genre, through="ProjectGenre")
    relations = models.ManyToManyField('self', through="TitleRelate", symmetrical=False, related_name="relation")

    class Meta:
        db_table = 'titles'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('project', kwargs={'slug_name': self.slug})

class Project(models.Model):
    def get_upload_path(instance, filename):
        return f"images/banners/{instance.title.id}.jpg"
    STATE_OF_PROJECT = (
        (0, 'Ukryty'),
        (1, 'Aktywny'),
        (2, 'Zakończony'),
        (3, 'Porzuczony'),
        (4, 'Zlicencjonowany') 
    )
    title = models.OneToOneField(Title, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(null=True, default=None, unique=True, populate_from='name')
    chapter_prefix = models.CharField(max_length=25)
    state = models.IntegerField(choices=STATE_OF_PROJECT)
    text_state = models.TextField(blank=True, null=True)
    banner = models.ImageField(null=True, upload_to=get_upload_path)
    objects = models.Manager()
    no_hentai = NonHentaiProjectsManager()
    single_project = SingleProjectManager()
            
    class Meta:
        db_table = 'projects'
    def __str__(self):
        return self.name
    def get_cover(self):
        return f'/media/images/covers/{self.title.id}/1.jpg'
    def get_absolute_url(self):
        return reverse('project', kwargs={'slug_name': self.slug})

class Author(models.Model):
    TYPE_OF_WORK = (
        (0, 'Author'),
        (1, 'Artist'),
        (2, 'Assistant')
    )
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    work = models.PositiveSmallIntegerField(choices=TYPE_OF_WORK)

    class Meta:
        db_table = 'authors'

    def __str__(self):
        return self.title.name + ' - ' + self.person.name


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'roles'
    def __str__(self):
        return self.job.name + '-' + self.project.name + '-' + self.user.name


class Volume(models.Model):
    def get_upload_path(instance, filename):
        return f"images/covers/{instance.project.title.id}/{instance.order_number}.jpg"

    id = models.AutoField(primary_key=True)
    order_number = models.IntegerField()
    number = models.IntegerField()
    specific_name = models.CharField(max_length=30, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    cover = models.ImageField(null=True, upload_to=get_upload_path)
    class Meta:
        db_table = 'volumes'
    def __str__(self):
        return self.project.name + "-" + str(self.order_number)

class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField()
    number = models.CharField(max_length=10, blank=True, null=True)
    prefix_title = models.CharField(max_length=20, blank=True, null=True)
    order_number = models.SmallIntegerField()
    volume = models.ForeignKey('Volume', on_delete=models.CASCADE)
    active = models.IntegerField()
    state = models.IntegerField()
    date = models.DateField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    class Meta:
        db_table = 'chapters'
    def __str__(self):
        return self.volume.project.name + "-" + str(self.volume.number) + '-' + str(self.order_number)
    

class ProjectGenre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    project = models.ForeignKey('Title', on_delete=models.CASCADE)

    class Meta:
        db_table = 'project_genre'
        unique_together = (('genre', 'project'),)
    def __str__(self):
        return self.project.name + "-" + self.genre.name


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    prev_work = models.ForeignKey('self', on_delete=models.CASCADE)

    class Meta:
        db_table = 'works'
        unique_together = (('user', 'chapter', 'job'),)
    def __str__(self):
        return self.chapter.name + "-" + self.job.name + '-' + self.user.name

class TitleRelate(models.Model):
    RELATION_TYPES = (
        (0, 'Doujin'),
        (1, "Sequel"),
        (2, "Prequel"),
        (3, "Historia poboczna")
    )
    title = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='title')
    title_related = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='title_related')
    relation_type = models.PositiveSmallIntegerField(choices=RELATION_TYPES)

    class Meta:
       db_table = 'title_relations'
    def __str__(self):
        return self.title.name + "-" + self.title_related.name + '-' + self.relation_type

class ProjectsInNeed(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    job_text = models.TextField()
    description = models.TextField()
    active = models.BooleanField(default=False)

    class Meta:
       db_table = 'projects-in-need'
    def __str__(self):
        return self.project.name