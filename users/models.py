from django.db import models

# Create your models here.

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=32)
    email = models.CharField(max_length=255)
    joining_date = models.DateField()
    quiting_date = models.DateField()
    avatar = models.CharField(max_length=255)
    admin = models.IntegerField()
    active = models.IntegerField()
    discord = models.CharField(max_length=60)

    class Meta:
        db_table = 'users'
        unique_together = (('name', 'email'),)

    def __str__(self):
        return self.name


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    hash = models.CharField(max_length=100)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'sessions'