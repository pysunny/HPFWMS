from django.db import models
from db.base_model import BaseModel

# Create your models here.
class Projects(BaseModel):
    """ 项目列表模型类 """
    LOCATION_CHOICES = (
        (0, 'HPF'),
        (1, 'HHKD'),
        (2, 'HGZ'),
        (3, 'HSH'),
        (4, 'HDL')
    )
    project_id = models.CharField(max_length=128, primary_key=True, verbose_name='工程编号')
    name = models.CharField(max_length=256, verbose_name='工程名称')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    address = models.CharField(max_length=256, default="", verbose_name='工程地址')
    projectlocation = models.SmallIntegerField(default=0, choices=LOCATION_CHOICES, verbose_name='项目区域')
    is_newversion = models.BooleanField(default=True, verbose_name='是否新项目')

    class Meta:
        db_table = 'df_projects'
        verbose_name = '项目列表'
        verbose_name_plural = verbose_name

class Favorites(BaseModel):
    """ 项目收藏夹模型类 """
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    project = models.ForeignKey('Projects', on_delete=models.CASCADE, verbose_name='项目')
    is_favorites = models.BooleanField(default=False, verbose_name='是否收藏')

    class Meta:
        db_table = 'df_favorites'
        verbose_name = '项目个人收藏夹'
        verbose_name_plural = verbose_name

class PdsVersion(BaseModel):
    """ 开工纸版本模型类 """
    project = models.ForeignKey('project.Projects', on_delete=models.CASCADE, verbose_name='所属项目')
    name = models.CharField(max_length=16, verbose_name='版本名称')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='修改者')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')
    setsSum = models.SmallIntegerField(default=0, verbose_name='总组数')
    areaSum = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='总面积')
    lengthSum = models.DecimalField(default=0, max_digits=5, decimal_places=2, verbose_name='总长度')
    panelSum = models.SmallIntegerField(default=0, verbose_name='总件数')
    lcpSum = models.SmallIntegerField(default=0, verbose_name='伸缩板件数')
    bpSum = models.SmallIntegerField(default=0, verbose_name='基本板件数')
    ipdSum = models.SmallIntegerField(default=0, verbose_name='门中门件数')
    bspSum = models.SmallIntegerField(default=0, verbose_name='波胶板件数')

    class Meta:
        db_table = 'df_pdsversion'
        verbose_name = '开工纸版本'
        verbose_name_plural = verbose_name