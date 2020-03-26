# Generated by Django 2.2.6 on 2020-03-03 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0007_panelmodels_paneltype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panelmodels',
            name='series',
            field=models.SmallIntegerField(choices=[(0, 'CT680'), (1, '5000'), (2, '600'), (3, 'Gl'), (4, 'GF'), (5, 'CTK'), (6, 'P5K'), (7, 'P6K')], verbose_name='系列'),
        ),
    ]