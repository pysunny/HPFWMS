from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.


class User(AbstractUser, BaseModel):
    """ 用户模型类 """
    LOCATION_CHOICES = (
        (0, 'HPF'),
        (1, 'HHKD'),
        (2, 'HGZ'),
        (3, 'HSH'),
        (4, 'HDL')
    )
    email_activate = models.BooleanField(default=False, verbose_name='电邮激活')
    location = models.SmallIntegerField(default=0, choices=LOCATION_CHOICES, verbose_name='所在区域')
    location_permiss = models.CharField(default='', max_length=256, verbose_name='区域权限')
    app_permiss = models.CharField(default='', max_length=256, verbose_name='app权限')

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
