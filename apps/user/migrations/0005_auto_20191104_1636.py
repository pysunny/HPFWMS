# Generated by Django 2.2.6 on 2019-11-04 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20191104_1413'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='app_permiass',
            new_name='app_permiss',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='location_permiass',
            new_name='location_permiss',
        ),
    ]