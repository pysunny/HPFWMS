from django.db import models
from django.db.models.fields import DateTimeField, DecimalField, related
from django.db.models.fields.related import ManyToManyField
class BaseModel(models.Model):
    """ 模型抽象基类 """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    # 添加转化字典的方法

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)

            if fields and f.name not in fields:
                continue

            if exclude and f.name in exclude:
                continue

            if isinstance(f, ManyToManyField):
                value = [ i.id for i in value ] if self.pk else None

            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None

            if isinstance(f, DecimalField):
                value = float(value)

            # 如果有选择值，直接返回对应的选项值
            if not f.choices == []:
                for tmp in f.choices:
                    if value == tmp[0]:
                        value = tmp[1]
        
            data[f.name] = value

        return data

    # 添加获取全部key的方法
    def get_key_list(self):
        data = []
        for f in self._meta.concrete_fields:
            if isinstance(f, related.ForeignKey):
                data.append('%s_id'% f.name)
            else:
                data.append(f.name)
        return data

    class Meta:
        # 说明是一个抽象模型类
        abstract = True