from django.db import models
from db.base_model import BaseModel

# Create your models here.
class Panelsets(BaseModel):
    """ 屏风组模型类 """
    # 多向式轮子
    OMNI_WHEEL_CHOICES = (
        (0,'26#'),
        (1,'36#'),
        (2,'57#'),
        (3,'11#'),
    )
    # 单向式轮子
    PAIR_WHEEL_CHOICES = (
        (4,'38#'),
        (5,'40#'),
        (6,'42#'),
        (7,'11T#')
    )
    # 全部轮子
    WHEEL_CHOICES = OMNI_WHEEL_CHOICES + PAIR_WHEEL_CHOICES

    FACE_STRUCTURE_CHOICES = (
        (0,'None(无钢结构)'),
        (1,'Skinned With Vertical Trim(固面带收边)'),
        (2,'Loose With Vertical Trim(易面带收边)'),
        (3,'Skinned Trimness(固面不带收边)')
    )
    SOUND_TEST_CHOICES = (
        (0,'No(不需要)'),
        (1,'Yes(需要)')
    )
    LOCKER_OPTION_CHOICES = (
        (0,'None(无)'), 
        (1,'Key(锁匙)'), 
        (2,'Knob(旋钮)')
    )
    project = models.ForeignKey('project.Projects', on_delete=models.CASCADE, verbose_name='所属项目')
    location = models.CharField(max_length=64, blank=True, verbose_name='区域名称')
    mark = models.CharField(max_length=128, verbose_name='屏风编号')
    sets = models.SmallIntegerField(default=1, verbose_name='组数')
    production_time = models.DateTimeField(verbose_name='出厂时间')
    model = models.ForeignKey('standard.PanelModels', on_delete=models.CASCADE, verbose_name='型号')
    height = models.IntegerField(verbose_name='高度')
    width = models.IntegerField(verbose_name='宽度')
    wheel = models.SmallIntegerField(choices=WHEEL_CHOICES, verbose_name='轮子')
    sound_test = models.SmallIntegerField(choices=SOUND_TEST_CHOICES, verbose_name='隔音测试')
    face_structure = models.SmallIntegerField(choices=FACE_STRUCTURE_CHOICES, blank=True, verbose_name='屏风结构')
    frame_color = models.CharField(max_length=128, verbose_name='边框颜色')
    splicer = models.CharField(max_length=128, default="无横驳条", verbose_name='横驳条分布')
    decoration_thickness = models.SmallIntegerField(default=0, verbose_name='装饰面厚度')
    decoration_text = models.CharField(max_length=256, blank=True, verbose_name='装饰面文字说明')
    note = models.CharField(max_length=1024, blank=True, verbose_name='备注信息')
    handle_quantity = models.SmallIntegerField(default=1, verbose_name='摇手柄数量')
    doorheight = models.CharField(max_length=64, blank=True, verbose_name='门中门门高')
    lockeyoption_a = models.SmallIntegerField(choices=LOCKER_OPTION_CHOICES, blank=True, default=None, verbose_name='A面锁类型')
    lockeyoption_b = models.SmallIntegerField(choices=LOCKER_OPTION_CHOICES, blank=True, default=None, verbose_name='B面锁类型')
    pdsversion = models.ForeignKey('project.pdsVersion', on_delete=models.CASCADE, verbose_name='开工纸版本')

    class Meta:
        db_table = 'df_panelsets'
        verbose_name = '屏风组列表'
        verbose_name_plural = verbose_name

class Panels(BaseModel):
    """ 屏风模型类 """
    PANEL_TYPE_CHOICES = (
        (0,'BP'),
        (1,'LCP'),
        (2,'BSP'),
        (3,'WJ'),
        (4,'UIPD'),
        (5,'LIPD'),
        (6,'FP')
    )
    panelset = models.ForeignKey(Panelsets, on_delete=models.CASCADE, verbose_name='所属屏风组')
    panle_no = models.CharField(max_length=64, verbose_name='屏风编号')
    quantity = models.SmallIntegerField(default=1, verbose_name='数量')
    carrier_space = models.CharField(max_length=64, verbose_name='轮距')
    panel_width = models.SmallIntegerField(verbose_name='屏风长度')
    panel_pic = models.ForeignKey('standard.PicsModels', default=1, on_delete=models.CASCADE, verbose_name='屏风图元')

    class Meta:
        db_table = 'df_panels'
        verbose_name = '屏风列表'
        verbose_name_plural = verbose_name
