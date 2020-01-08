# Generated by Django 2.2.6 on 2019-12-27 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0003_favorites_is_favorites'),
        ('standard', '0005_auto_20191227_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Panelsets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('location', models.CharField(blank=True, max_length=64, verbose_name='区域名称')),
                ('mark', models.CharField(max_length=128, verbose_name='屏风编号')),
                ('sets', models.SmallIntegerField(default=1, verbose_name='组数')),
                ('production_time', models.DateTimeField(verbose_name='出厂时间')),
                ('height', models.IntegerField(verbose_name='高度')),
                ('width', models.IntegerField(verbose_name='宽度')),
                ('wheel', models.SmallIntegerField(choices=[(0, '26#'), (1, '36#'), (2, '57#'), (3, '11#'), (4, '38#'), (5, '40#'), (6, '42#'), (7, '11T#')], verbose_name='轮子')),
                ('sound_test', models.SmallIntegerField(choices=[(0, 'No(不需要)'), (1, 'Yes(需要)')], verbose_name='隔音测试')),
                ('face_structure', models.SmallIntegerField(blank=True, choices=[(0, 'None(无钢结构)'), (1, 'Skinned With Vertical Trim(固面带收边)'), (2, 'Loose With Vertical Trim(易面带收边)'), (3, 'Skinned Trimness(固面不带收边)')], verbose_name='屏风结构')),
                ('frame_color', models.CharField(max_length=128, verbose_name='边框颜色')),
                ('splicer', models.CharField(default='无横驳条', max_length=128, verbose_name='横驳条分布')),
                ('decoration_thickness', models.SmallIntegerField(default=0, verbose_name='装饰面厚度')),
                ('decoration_text', models.CharField(blank=True, max_length=256, verbose_name='装饰面文字说明')),
                ('note', models.CharField(blank=True, max_length=1024, verbose_name='备注信息')),
                ('handle_quantity', models.SmallIntegerField(default=1, verbose_name='摇手柄数量')),
                ('doorheight', models.CharField(blank=True, max_length=64, verbose_name='门中门门高')),
                ('lockeyoption_a', models.SmallIntegerField(blank=True, choices=[(0, 'None(无)'), (1, 'Key(锁匙)'), (2, 'Knob(旋钮)')], default=None, verbose_name='A面锁类型')),
                ('lockeyoption_b', models.SmallIntegerField(blank=True, choices=[(0, 'None(无)'), (1, 'Key(锁匙)'), (2, 'Knob(旋钮)')], default=None, verbose_name='B面锁类型')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standard.PanelModels', verbose_name='型号')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Projects', verbose_name='所属项目')),
            ],
            options={
                'db_table': 'df_panelsets',
                'verbose_name': '屏风组列表',
                'verbose_name_plural': '屏风组列表',
            },
        ),
        migrations.CreateModel(
            name='Panels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('is_delete', models.BooleanField(default=False, verbose_name='删除标记')),
                ('panle_no', models.CharField(max_length=64, verbose_name='屏风编号')),
                ('quantity', models.SmallIntegerField(default=1, verbose_name='数量')),
                ('carrier_space', models.CharField(max_length=64, verbose_name='轮距')),
                ('panel_width', models.SmallIntegerField(verbose_name='屏风长度')),
                ('panel_type', models.SmallIntegerField(choices=[(0, 'BP'), (1, 'LCP'), (2, 'BSP'), (3, 'WJ'), (4, 'UIPD'), (5, 'LIPD'), (6, 'FP')], verbose_name='屏风类型')),
                ('panel_pic', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='standard.PicsModels', verbose_name='屏风图元')),
                ('panelset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PDS.Panelsets', verbose_name='所属屏风组')),
            ],
            options={
                'db_table': 'df_panels',
                'verbose_name': '屏风列表',
                'verbose_name_plural': '屏风列表',
            },
        ),
    ]
