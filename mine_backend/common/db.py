from django.db import models


class BaseModel(models.Model):
    # 抽象的模型基类，定义一些公共的模型字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 软删除，删除是将这个字段设置为True，而非物理删除
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        abstract = True  # 说明是抽象模型类，用于继承使用，数据库迁移时不会创建BaseModel的表
        verbose_name_plural = "公共字段模型"
        db_table = "BaseTable"
