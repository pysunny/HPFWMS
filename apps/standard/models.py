from django.db import models
from db.base_model import BaseModel

# Create your models here.
class PanelModels(BaseModel):
    """ 屏风标准型号模型类 """
    SERIES_CHOICES = (
        (0,'ct680'),
        (1,'5000'),
        (2,'600')
    )
    BASIC_MATERIAL_CHOICES = (
        (0,'石膏板'),
        (1,'木夹板'),
        (3,'无')
    )
    STEEL_PLATE_CHOICES = (
        (0,'内'),
        (1,'外'),
        (2,'无')
    )
    name = models.CharField(max_length=128, verbose_name='型号名称')
    series = models.SmallIntegerField(choices=SERIES_CHOICES, verbose_name='系列')
    desc = models.CharField(max_length=256, verbose_name='型号描述')
    bottom_seal = models.BooleanField(verbose_name='有无底胶')
    top_seal = models.BooleanField(verbose_name='有无顶胶')
    top_mechanism = models.BooleanField(verbose_name='有无顶撑')
    top_clearance = models.SmallIntegerField(verbose_name='顶部虚位')
    bottom_mechanism = models.BooleanField(verbose_name='有无底撑')
    bottom_clearance = models.SmallIntegerField(verbose_name='底部虚位')
    basic_material = models.SmallIntegerField(choices=BASIC_MATERIAL_CHOICES, verbose_name='基本板材')
    steel_plate = models.SmallIntegerField(choices=STEEL_PLATE_CHOICES, verbose_name='钢板')
    rockwool = models.BooleanField(verbose_name='有无岩棉')

    class Meta:
        db_table = 'df_models'
        verbose_name = '屏风模型'
        verbose_name_plural = verbose_name


class PartPicModels(BaseModel):
    """ 屏风图元组件类型类 """
    # 屏风种类选择
    PANEL_TYPE_CHOICES = (
        (0,'CommonPanels'),
        (1,'GlassPanels'),
        (2,'PocketDoor')
    )
    # 组件位置选择
    PIC_PART_CHOICES = (
        (0,'LeftSide'),
        (1,'MiddleBody'),
        (2,'Wheel'),
        (3,'RightSide')
    )
    name = models.CharField(max_length=256, verbose_name='组件名称标识')
    paneltype = models.SmallIntegerField(choices=PANEL_TYPE_CHOICES, verbose_name='屏风种类')
    panelpart = models.SmallIntegerField(choices=PIC_PART_CHOICES, verbose_name='组件位置')
    svgcode = models.CharField(max_length=512, verbose_name='图元组件代码')

    class Meta:
        db_table = 'df_svgparts'
        verbose_name = '图元组件模型'
        verbose_name_plural = verbose_name


class PicsModels(BaseModel):
    """ 屏风图元类型类 """
    # 屏风种类选择
    PANEL_TYPE_CHOICES = (
        (0,'CommonPanels'),
        (1,'GlassPanels'),
        (2,'PocketDoor')
    )
    PIC_TYPE_CHOICES = (
        (0,'BP'),
        (1,'LCP'),
        (2,'BSP'),
        (3,'WJ'),
        (4,'UIPD'),
        (5,'LIPD'),
        (6,'FP')
    )
    WHEEL_TYPE_CHOICES = (
        (0,'DOULE'),
        (1,'SINGLE')
    )
    name = models.CharField(max_length=256, verbose_name='组件名称标识')
    paneltype = models.SmallIntegerField(choices=PANEL_TYPE_CHOICES, verbose_name='屏风种类')
    wheeltype = models.SmallIntegerField(choices=WHEEL_TYPE_CHOICES, verbose_name='轮子分类')
    pictype = models.SmallIntegerField(choices=PIC_TYPE_CHOICES, verbose_name='图元种类')
    leftside = models.ForeignKey(PartPicModels, default=0, on_delete=models.CASCADE, verbose_name='左边组件图元', related_name="leftside")
    middle = models.ForeignKey(PartPicModels, default=0, on_delete=models.CASCADE, verbose_name='中间组件图元', related_name="middle")
    rightside = models.ForeignKey(PartPicModels, default=0, on_delete=models.CASCADE, verbose_name='右边组件图元', related_name="rightside")
    wheel = models.ForeignKey(PartPicModels, default=0, on_delete=models.CASCADE, verbose_name='轮子组件图元', related_name="wheel")
    extra_length = models.SmallIntegerField(default=0, verbose_name='额外长度')

    class Meta:
        db_table = 'df_pics'
        verbose_name = '图元模型'
        verbose_name_plural = verbose_name



        