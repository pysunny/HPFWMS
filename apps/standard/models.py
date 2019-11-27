from django.db import models
from db.base_model import BaseModel

# Create your models here.
class PanelModels(BaseModel):
    """ 屏风标准型号模型类 """
    SERIES_CHOICES = (
        (0,'CT680'),
        (1,'5000'),
        (2,'600')
    )
    BASIC_MATERIAL_CHOICES = (
        (0,'石膏板'),
        (1,'木夹板'),
        (2,'无')
    )
    STEEL_PLATE_CHOICES = (
        (0,'内'),
        (1,'外'),
        (2,'无')
    )
    TOP_OPTION_CHOICES = (
        (0,'机动顶撑 带 胶条'),
        (1,'机动顶撑 不带 胶条'),
        (2,'胶条'),
        (3,'电动顶撑 带 胶条'),
        (4,'电动顶撑 不带 胶条')
    )
    BOTTOM_OPTION_CHOICES = (
        (0,'机动底撑 带 胶条'),
        (1,'机动底撑 不带 胶条'),
        (2,'胶条'),
        (3,'电动底撑 带 胶条'),
        (4,'电动底撑 不带 胶条')
    )
    WHEEL_TYPE_CHOICES = (
        (0,'多向式'),
        (1,'单向式')
    )
    ROCKWOOL_CHOICES = (
        (0, '50kg岩棉'),
        (1, '无岩棉')
    )
    name = models.CharField(max_length=128, verbose_name='型号名称')
    series = models.SmallIntegerField(choices=SERIES_CHOICES, verbose_name='系列')
    desc = models.CharField(max_length=256, verbose_name='型号描述')
    bottom_option = models.SmallIntegerField(choices=BOTTOM_OPTION_CHOICES, default=0, verbose_name='底部选项')
    bottom_clearance = models.SmallIntegerField(verbose_name='底部虚位')
    top_option = models.SmallIntegerField(choices=TOP_OPTION_CHOICES, default=0, verbose_name='顶部选项')
    top_clearance = models.SmallIntegerField(verbose_name='顶部虚位')
    basic_material = models.SmallIntegerField(choices=BASIC_MATERIAL_CHOICES, verbose_name='基本板材')
    steel_plate = models.SmallIntegerField(choices=STEEL_PLATE_CHOICES, verbose_name='钢板')
    rockwool = models.SmallIntegerField(choices=ROCKWOOL_CHOICES, verbose_name='有无岩棉')
    wheel_type = models.SmallIntegerField(choices=WHEEL_TYPE_CHOICES, verbose_name='屏风类型', default=0)
    is_activate = models.BooleanField(default=False, verbose_name='激活标记')
    creator = models.ForeignKey('user.User', default=2, on_delete=models.CASCADE, verbose_name='创建者')

    class Meta:
        db_table = 'df_models'
        verbose_name = '屏风模型'
        verbose_name_plural = verbose_name


class PartPicModels(BaseModel):
    """ 屏风图元组件类型类 """
    # 屏风种类选择
    PANEL_TYPE_CHOICES = (
        (0,'普通屏风'),
        (1,'玻璃屏风'),
        (2,'收板间门')
    )
    # 组件位置选择
    PIC_PART_CHOICES = (
        (0,'左边'),
        (1,'中间'),
        (2,'轮子'),
        (3,'右边'),
        (4,'文字')
    )
    name = models.CharField(max_length=256, verbose_name='组件名称标识')
    paneltype = models.SmallIntegerField(choices=PANEL_TYPE_CHOICES, verbose_name='屏风种类')
    panelpart = models.SmallIntegerField(choices=PIC_PART_CHOICES, verbose_name='组件位置')
    svgcode = models.CharField(max_length=512, verbose_name='图元组件代码')
    is_activate = models.BooleanField(default=False, verbose_name='激活标记')
    creator = models.ForeignKey('user.User', default=2, on_delete=models.CASCADE, verbose_name='创建者')

    class Meta:
        db_table = 'df_svgparts'
        verbose_name = '图元组件模型'
        verbose_name_plural = verbose_name


class PicsModels(BaseModel):
    """ 屏风图元类型类 """
    # 屏风种类选择
    PANEL_TYPE_CHOICES = PartPicModels.PANEL_TYPE_CHOICES
    WHEEL_TYPE_CHOICES = PanelModels.WHEEL_TYPE_CHOICES
    PIC_TYPE_CHOICES = (
        (0,'BP'),
        (1,'LCP'),
        (2,'BSP'),
        (3,'WJ'),
        (4,'UIPD'),
        (5,'LIPD'),
        (6,'FP')
    )
    name = models.CharField(max_length=256, verbose_name='组件名称标识')
    paneltype = models.SmallIntegerField(choices=PANEL_TYPE_CHOICES, verbose_name='屏风种类')
    wheeltype = models.SmallIntegerField(choices=WHEEL_TYPE_CHOICES, verbose_name='轮子分类')
    pictype = models.SmallIntegerField(choices=PIC_TYPE_CHOICES, verbose_name='图元种类')
    leftside = models.ForeignKey(PartPicModels, on_delete=models.CASCADE, verbose_name='左边组件图元', related_name="leftside")
    middle = models.ForeignKey(PartPicModels, on_delete=models.CASCADE, verbose_name='中间组件图元', related_name="middle")
    rightside = models.ForeignKey(PartPicModels, on_delete=models.CASCADE, verbose_name='右边组件图元', related_name="rightside")
    wheel = models.ForeignKey(PartPicModels, on_delete=models.CASCADE, verbose_name='轮子组件图元', related_name="wheel")
    text = models.ForeignKey(PartPicModels, on_delete=models.CASCADE, verbose_name='文字组件图元', related_name="text")
    extra_length = models.SmallIntegerField(default=0, verbose_name='额外长度')
    pin_mark = models.BooleanField(default=False, verbose_name='是否有地针')
    is_activate = models.BooleanField(default=False, verbose_name='激活标记')
    creator = models.ForeignKey('user.User', default=2, on_delete=models.CASCADE, verbose_name='创建者')

    class Meta:
        db_table = 'df_pics'
        verbose_name = '图元模型'
        verbose_name_plural = verbose_name



        