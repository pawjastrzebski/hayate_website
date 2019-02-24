# Generated by Django 2.1.7 on 2019-02-24 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hash', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'sessions',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('password', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=255)),
                ('joining_date', models.DateField()),
                ('quiting_date', models.DateField()),
                ('avatar', models.CharField(max_length=255)),
                ('admin', models.IntegerField()),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('name', 'email')},
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.User'),
        ),
    ]
