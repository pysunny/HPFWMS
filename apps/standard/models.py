from django.db import models
from db.base_model import BaseModel

# Create your models here.
class PanelModels(BaseModel):
    """ 屏风标准型号模型类 """
    series_choices = (
        (0,'ct680'),
        (1,'5000'),
        (2,'600')
    )
    basic_material_choices = (
        (0,'石膏板'),
        (1,'木夹板'),
        (2,'无')
    )
    steel_plate_choices = (
        (0,'内'),
        (1,'外'),
        (2,'无')
    )
    name = models.CharField(max_length=256, verbose_name='型号名称')
    series = models.SmallIntegerField(choices=series_choices, verbose_name='系列')
    desc = models.CharField(max_length=256, verbose_name='型号描述')
    bottom_seal = models.BooleanField(verbose_name='有无底胶')
    top_seal = models.BooleanField(verbose_name='有无顶胶')
    top_mechanism = models.BooleanField(verbose_name='有无顶撑')
    top_clearance = models.IntegerField(verbose_name='顶部虚位')
    bottom_mechanism = models.BooleanField(verbose_name='有无底撑')
    bottom_clearance = models.IntegerField(verbose_name='底部虚位')
    basic_material = models.SmallIntegerField(choices=basic_material_choices, verbose_name='基本板材')
    steel_plate = models.SmallIntegerField(choices=steel_plate_choices, verbose_name='钢板')
    rockwool = models.BooleanField(verbose_name='有无岩棉')

    class Meta:
        db_table = 'df_models'
        verbose_name = '屏风模型'
        verbose_name_plural = verbose_name