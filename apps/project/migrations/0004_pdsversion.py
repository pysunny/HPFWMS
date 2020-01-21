# Generated by Django 2.2.6 on 2020-01-08 16:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0003_favorites_is_favorites'),
    ]

    operations = [
        migrations.CreateModel(
            name='pdsVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('name', models.CharField(max_length=16, verbose_name='版本名称')),
                ('is_public', models.BooleanField(default=False, verbose_name='是否公开')),
                ('setsSum', models.SmallIntegerField(verbose_name='总组数')),
                ('areaSum', models.DecimalField(decimal_places=2, max_digits=5)),
                ('lengthSum', models.DecimalField(decimal_places=2, max_digits=5)),
                ('panelSum', models.SmallIntegerField(verbose_name='总件数')),
                ('lcpSum', models.SmallIntegerField(verbose_name='伸缩板件数')),
                ('bpSum', models.SmallIntegerField(verbose_name='基本板件数')),
                ('ipdSum', models.SmallIntegerField(verbose_name='门中门件数')),
                ('bspSum', models.SmallIntegerField(verbose_name='波胶板件数')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects', verbose_name='所属项目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='修改者')),
            ],
            options={
                'db_table': 'df_pdsversion',
                'verbose_name': '开工纸版本',
                'verbose_name_plural': '开工纸版本',
            },
        ),
    ]
