# Generated by Django 2.2.6 on 2019-11-14 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standard', '0011_auto_20191113_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partpicmodels',
            name='panelpart',
            field=models.SmallIntegerField(choices=[(0, '左边'), (1, '中间'), (2, '轮子'), (3, '右边'), (4, '文字')], verbose_name='组件位置'),
        ),
        migrations.AlterField(
            model_name='partpicmodels',
            name='paneltype',
            field=models.SmallIntegerField(choices=[(0, '普通屏风'), (1, '玻璃屏风'), (2, '收板间门')], verbose_name='屏风种类'),
        ),
    ]