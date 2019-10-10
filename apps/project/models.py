from django.db import models
from db.base_model import BaseModel

# Create your models here.
class Projects(BaseModel):
    """ 项目列表模型类 """
    project_id = models.CharField(max_length=128, primary_key=True, verbose_name='工程编号')
    name = models.CharField(max_length=256, verbose_name='工程名称')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    address = models.CharField(max_length=256, default="", verbose_name='工程地址')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')

    class Meta:
        db_table = 'df_projects'
        verbose_name = '项目列表'
        verbose_name_plural = verbose_name

