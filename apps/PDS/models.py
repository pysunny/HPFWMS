from django.db import models
from db.base_model import BaseModel

# Create your models here.
class Panelsets(BaseModel):
    """ 屏风组模型类 """
    WHEEL_CHOICES = (
        (0,'26'),
        (1,'36'),
        (2,'57'),
        (3,'11'),
        (4,'38'),
        (5,'40'),
        (6,'42'),
        (7,'11T')
    )
    FACE_STRUCTURE_CHOICES = (
        (0,'没钢结构'),
        (1,'固面带收边'),
        (2,'易面带收边'),
        (3,'固面不带收边')
    )
    SOUND_TEST_CHOICES = (
        (0,'不需要'),
        (1,'需要')
    )
    project = models.ForeignKey('project.Projects', on_delete=models.CASCADE, verbose_name='所属项目')
    mark = models.CharField(max_length=128, verbose_name='屏风编号')
    sets = models.SmallIntegerField(default=1, verbose_name='组数')
    production_time = models.DateField(verbose_name='出厂时间')
    model = models.ForeignKey('standard.PanelModels', on_delete=models.CASCADE, verbose_name='型号')
    height = models.IntegerField(verbose_name='高度')
    width = models.IntegerField(verbose_name='宽度')
    wheel = models.SmallIntegerField(choices=WHEEL_CHOICES, verbose_name='轮子')
    sound_test = models.SmallIntegerField(choices=SOUND_TEST_CHOICES, verbose_name='隔音测试')
    face_structure = models.SmallIntegerField(choices=FACE_STRUCTURE_CHOICES, verbose_name='屏风结构')
    frame_color = models.CharField(max_length=128, verbose_name='边框颜色')
    splicer = models.CharField(max_length=128, default="", verbose_name='横驳条分布')

    class Meta:
        db_table = 'df_panelsets'
        verbose_name = '屏风组列表'
        verbose_name_plural = verbose_name

class Panles(BaseModel):
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
    panle_no = models.CharField(max_length=128, verbose_name='屏风编号')
    quantity = models.SmallIntegerField(default=1, verbose_name='数量')
    carrier_space = models.SmallIntegerField(verbose_name='轮距')
    panel_width = models.SmallIntegerField(verbose_name='屏风长度')
    panel_type = models.SmallIntegerField(choices=PANEL_TYPE_CHOICES, verbose_name='屏风类型')
    panel_pic = models.ForeignKey('standard.PicsModels', default=1, on_delete=models.CASCADE, verbose_name='屏风图元')

    class Meta:
        db_table = 'df_panels'
        verbose_name = '屏风列表'
        verbose_name_plural = verbose_name