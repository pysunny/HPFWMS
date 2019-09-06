from django.db import models
from db.base_model import BaseModel

# Create your models here.
class Projects(BaseModel):
    """ 项目列表模型类 """
    name = models.CharField(max_length=256, verbose_name='工程名称')
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, verbose_name='用户')
    request_time = models.DateTimeField(verbose_name='出厂时间')
    is_public = models.BooleanField(default=False, verbose_name='是否公开')

    class Meta:
        db_table = 'df_project_list'
        verbose_name = '项目列表'
        verbose_name_plural = verbose_name

