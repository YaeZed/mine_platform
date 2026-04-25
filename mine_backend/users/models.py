from django.db import models
from common.db import BaseModel
# django中自带的用户认证模型
from django.contrib.auth.models import AbstractUser


class User(AbstractUser, BaseModel):
    # 扩展用户模型，settings.py中AUTH_USER_MODEL = 'users.User'
    mobile = models.CharField(max_length=11, verbose_name='手机号', default='')
    avatar = models.ImageField(verbose_name='用户头像', blank=True, null=True)
    nickname = models.CharField(max_length=11, verbose_name='<UNK>', default='')
    class Meta:
        db_table = 'user'
        verbose_name = '用户表'


class VerifyCode(models.Model):
    # 验证码模型
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    code = models.CharField(max_length=6, verbose_name='验证码')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='生成时间')

    class Meta:
        db_table = 'verify_code'
        verbose_name = '验证码表'
