# Generated by Django 2.2.6 on 2019-12-06 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PDS', '0003_auto_20191129_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panels',
            name='carrier_space',
            field=models.CharField(max_length=64, verbose_name='轮距'),
        ),
        migrations.AlterField(
            model_name='panels',
            name='panle_no',
            field=models.CharField(max_length=64, verbose_name='屏风编号'),
        ),
    ]