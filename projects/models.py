from django.db import models
from users.models import User


class Genre(models.Model):
    TYPES_OF_GENRE = (
        (0, "gatunek"),
        (1, "grupa demograficzna"),
        (2, "czasy"),
        (3, "miejsce"),
        (4, "inne")
    )
    id = models.AutoField(primary_key=True)
    genre_type = models.PositiveIntegerField(blank=True, null=True, choices=TYPES_OF_GENRE)
    name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'genres'


class Job(models.Model):
    id = models.AutoField(primary_key=True)
    job_name = models.CharField(max_length=50)
    hide = models.IntegerField()
    new_column = models.IntegerField()

    class Meta:
        db_table = 'jobs'


class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    deep = models.IntegerField()
    menu_url = models.CharField(max_length=100)
    menu_name = models.CharField(max_length=150)
    hide = models.IntegerField()

    class Meta:
        db_table = 'menu'
        unique_together = (('id', 'deep'),)


class Project(models.Model):
    STATE_OF_PROJECT = (
        (0, 'ukryty'),
        (1, 'aktywny'),
        (2, 'zakończony'),
        (3, 'porzuczony'),
        (4, 'zlicencjonowany') 
    )
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=255)
    name = models.CharField(unique=True, max_length=255)
    name_pl = models.CharField(db_column='long_name_PL', max_length=255)
    name_en = models.CharField(db_column='long_name_EN', max_length=255)
    chapter_prefix = models.CharField(max_length=25)
    state = models.IntegerField(choices=STATE_OF_PROJECT)
    type = models.IntegerField()
    age_limit = models.IntegerField()
    author = models.SmallIntegerField()
    artist = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    total_volumes = models.SmallIntegerField()
    state_japan = models.IntegerField()
    text_state = models.TextField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, through="ProjectGenre")

    class Meta:
        db_table = 'projects'
    def __str__(self):
            return self.short_name





class Role(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'roles'


class Volume(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.IntegerField()
    number = models.IntegerField()
    specific_name = models.CharField(max_length=30, blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        db_table = 'volumes'


class Chapter(models.Model):
    id = models.AutoField(primary_key=True)
    filename = models.CharField(max_length=255, blank=True, null=True)
    title = models.TextField()
    number = models.SmallIntegerField()
    prefix_title = models.CharField(max_length=20, blank=True, null=True)
    order_number = models.SmallIntegerField()
    volume = models.SmallIntegerField()
    new = models.IntegerField()
    state = models.IntegerField()
    date = models.IntegerField()
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        db_table = 'chapters'
        unique_together = (('id', 'new'), ('project', 'number', 'prefix_title', 'volume'),)

class ProjectGenre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    class Meta:
        db_table = 'project_genre'
        unique_together = (('genre', 'project'),)


class Work(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    chapter = models.ForeignKey('Chapter', on_delete=models.CASCADE)
    job = models.ForeignKey('Job', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'works'
        unique_together = (('user', 'chapter', 'job'),)


class Person(models.Model):
    BLOOD_TYPE = (
        (0, "0"),
        (1, "A"),
        (2, "B"),
        (3, "AB")
    )   
    name = models.CharField(max_length=100)
    birthplace = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField()
    blood_type = models.CharField(max_length=2, blank=True, null=True, choices=BLOOD_TYPE)
    description = models.TextField()
  #  project = models.ManyToManyField(Project, through='Author')

    class Meta:
        db_table = 'people'


class Authors(models.Model):
    TYPE_OF_WORK = (
        (0, 'Author'),
        (1, 'Artist'),
        (2, 'Assistant')
    )
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    description = models.TextField()
    work = models.PositiveSmallIntegerField(choices=TYPE_OF_WORK)

    class Meta:
        db_table = 'authors'
