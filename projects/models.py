from django.db import models
from users.models import User
from autoslug import AutoSlugField
from django.urls import reverse


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

    


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    hide = models.IntegerField()

    class Meta:
        db_table = 'jobs'

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


class Volume(models.Model):
    def get_upload_path(instance, filename):
        return f"images/covers/{instance.project.id}/{instance.order_number}.jpg"

    id = models.AutoField(primary_key=True)
    order_number = models.IntegerField()
    number = models.IntegerField()
    specific_name = models.CharField(max_length=30, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    cover = models.ImageField(null=True, upload_to=get_upload_path)
    class Meta:
        db_table = 'volumes'

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
    date = models.IntegerField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    class Meta:
        db_table = 'chapters'

class ProjectGenre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    project = models.ForeignKey('Title', on_delete=models.CASCADE)

    class Meta:
        db_table = 'project_genre'
        unique_together = (('genre', 'project'),)


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