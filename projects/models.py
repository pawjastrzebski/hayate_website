from django.db import models


class Genres(models.Model):
    TYPES_OF_GENRE = (
        (0, "gatunek"),
        (1, "grupa demograficzna"),
        (2, "czasy"),
        (3, "miejsce"),
        (4, "inne")
    )
    id = models.AutoField(primary_key=True)
    genre_type = models.PositiveIntegerField(blank=True, null=True, choices=TYPES_OF_GENRE)
    genre_name = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        db_table = 'genres'


class Jobs(models.Model):
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


class Projects(models.Model):
    STATE_OF_PROJECT = (
        (0, 'ukryty'),
        (1, 'aktywny'),
        (2, 'zakończony'),
        (3, 'porzuczony'),
        (4, 'zlicencjonowany') 
    )
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=255)
    long_name = models.CharField(unique=True, max_length=255)
    long_name_pl = models.CharField(db_column='long_name_PL', max_length=255)
    long_name_en = models.CharField(db_column='long_name_EN', max_length=255)
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

    class Meta:
        db_table = 'projects'


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=40)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=255)
    joining_date = models.DateField()
    quiting_date = models.DateField()
    avatar = models.CharField(max_length=255)
    admin = models.IntegerField()

    class Meta:
        db_table = 'users'
        unique_together = (('nickname', 'email'),)


class Sessions(models.Model):
    id = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=100)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sessions'


class Roles(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.TextField()
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)

    class Meta:
        db_table = 'roles'


class Volumes(models.Model):
    id = models.AutoField(primary_key=True)
    order_number = models.IntegerField()
    number = models.IntegerField()
    specific_name = models.CharField(max_length=30, blank=True, null=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

    class Meta:
        db_table = 'volumes'


class Chapters(models.Model):
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
    project = models.ForeignKey('Projects', on_delete=models.CASCADE)

    class Meta:
        db_table = 'chapters'
        unique_together = (('id', 'new'), ('project', 'number', 'prefix_title', 'volume'),)


class ProjectGenre(models.Model):
    id = models.AutoField(primary_key=True)
    genre = models.ForeignKey('Genres', on_delete=models.CASCADE)
    project = models.ForeignKey('Projects', on_delete=models.CASCADE)

    class Meta:
        db_table = 'project_genre'
        unique_together = (('genre', 'project'),)


class Works(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    chapter = models.ForeignKey('Chapters', on_delete=models.CASCADE)
    job = models.ForeignKey('Jobs', on_delete=models.CASCADE)
    user = models.ForeignKey('Users', on_delete=models.CASCADE)

    class Meta:
        db_table = 'works'
        unique_together = (('user', 'chapter', 'job'),)


class People(models.Model):
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
    projects = models.ManyToManyField(Projects, through='Authors')

    class Meta:
        db_table = 'people'


class Authors(models.Model):
    TYPE_OF_WORK = (
        (0, 'Author'),
        (1, 'Artist'),
        (2, 'Assistant')
    )
    person = models.ForeignKey('People', on_delete=models.CASCADE)
    project = models.ForeignKey('Projects', on_delete=models.CASCADE)
    description = models.TextField()
    work = models.PositiveSmallIntegerField(choices=TYPE_OF_WORK)

    class Meta:
        db_table = 'authors'
