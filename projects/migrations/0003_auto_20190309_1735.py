# Generated by Django 2.1.7 on 2019-03-09 16:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20190309_0318'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectsInNeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'projects-in-need',
            },
        ),
        migrations.AlterModelManagers(
            name='project',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='projectsinneed',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.AddField(
            model_name='projectsinneed',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Role'),
        ),
    ]