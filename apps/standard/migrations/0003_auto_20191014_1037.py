# Generated by Django 2.2.6 on 2019-10-14 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0002_partpicmodels'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partpicmodels',
            old_name='pinPart',
            new_name='panelPart',
        ),
    ]