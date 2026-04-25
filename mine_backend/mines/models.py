from django.db import models


class Mine(models.Model):
    mine_id = models.AutoField(primary_key=True, verbose_name='矿井ID')
    mine_username = models.CharField(max_length=50, verbose_name='矿井所属用户')
    mine_name = models.CharField(max_length=50, verbose_name='矿井名称')
    mine_desc = models.CharField(max_length=200, verbose_name='矿井描述')

    class Meta:
        db_table = 'Mine'
        verbose_name_plural = '矿井表'


class ThreeDMineTunnel(models.Model):
    id = models.AutoField(primary_key=True)
    tube_wind_speed = models.CharField(max_length=255, verbose_name='风速')
    tube_R = models.CharField(max_length=255, verbose_name='R值')
    tube_H = models.CharField(max_length=255, verbose_name='H值')
    point_left_x = models.CharField(max_length=255, verbose_name='左上角X坐标')
    point_left_y = models.CharField(max_length=255, verbose_name='左上角Y坐标')
    point_left_z = models.CharField(max_length=255, verbose_name='左上角Z坐标')
    point_right_x = models.CharField(max_length=255, verbose_name='右上角X坐标')
    point_right_y = models.CharField(max_length=255, verbose_name='右上角Y坐标')
    point_right_z = models.CharField(max_length=255, verbose_name='右上角Z坐标')
    tube_name = models.CharField(max_length=255, verbose_name='隧道名称')

    class Meta:
        db_table = 'ThreeDMineTunnel'
        verbose_name_plural = '三维矿井隧道坐标'


class Node(models.Model):
    node_id = models.AutoField(primary_key=True)
    x = models.FloatField(verbose_name='x坐标')
    y = models.FloatField(verbose_name='y坐标')
    z = models.FloatField(verbose_name='z坐标')
    class Meta:
        db_table = 'Node'
        verbose_name_plural = '节点坐标'

class Tunnel(models.Model):
    tunnel_id = models.AutoField(primary_key=True)
    start_id = models.IntegerField(verbose_name='起点ID')
    end_id = models.IntegerField(verbose_name='终点ID')
    r = models.FloatField(verbose_name='阻力系数')
    q = models.FloatField(verbose_name='风量',null=True)
    h = models.FloatField(verbose_name='阻力',null=True)
    class Meta:
        db_table = 'Tunnel'
        verbose_name_plural = '巷道信息'
