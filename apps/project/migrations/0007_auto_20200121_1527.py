# Generated by Django 2.2.6 on 2020-01-21 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_projects_lastversion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projects',
            name='lastversion',
        ),
        migrations.AddField(
            model_name='projects',
            name='is_newversion',
            field=models.BooleanField(default=True, verbose_name='是否新项目'),
        ),
    ]