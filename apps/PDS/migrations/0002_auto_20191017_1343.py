# Generated by Django 2.2.6 on 2019-10-17 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PDS', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panelsets',
            name='mark',
            field=models.CharField(max_length=128, verbose_name='屏风编号'),
        ),
    ]