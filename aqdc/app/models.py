# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AqiInfo(models.Model):
    city_code = models.IntegerField(primary_key=True, verbose_name='城市/区域代码')
    date = models.DateField(db_column='DATE', verbose_name='日期')  # Field name made lowercase.
    aqi = models.IntegerField(verbose_name='AQI')
    pri_pollutant = models.CharField(max_length=15, verbose_name='首要污染物')

    class Meta:
        verbose_name = 'AQI信息'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'aqi_info'
        unique_together = (('city_code', 'date'),)


class CityProv(models.Model):
    city_code = models.IntegerField(primary_key=True, verbose_name='城市/区域码')
    city_name = models.CharField(max_length=30, verbose_name='城市/区域名称')
    prov_name = models.ForeignKey('Prov', models.DO_NOTHING, db_column='prov_name', verbose_name='所属省级行政区')
    longitude = models.FloatField(verbose_name='经度')
    latitude = models.FloatField(verbose_name='纬度')

    class Meta:
        verbose_name = '市属关系'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'city_prov'


class CurData(models.Model):
    city_code = models.IntegerField(primary_key=True, verbose_name='城市/区域码')
    time = models.DateTimeField(verbose_name='时间')
    aqi = models.IntegerField(verbose_name='AQI')
    pm2_5 = models.IntegerField(verbose_name='PM2.5')
    pm10 = models.IntegerField(verbose_name='PM10')
    so2 = models.FloatField(verbose_name='二氧化硫')
    no2 = models.FloatField(verbose_name='二氧化氮')
    co = models.FloatField(verbose_name='一氧化碳')
    o3 = models.FloatField(verbose_name='臭氧')
    pri_pollutant = models.CharField(max_length=15, verbose_name='首要污染物')

    class Meta:
        verbose_name = '实时数据'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'cur_data'
        unique_together = (('city_code', 'time'),)


class Prov(models.Model):
    prov_name = models.CharField(primary_key=True, max_length=12, verbose_name='省级区域名')
    prov_cap = models.CharField(unique=True, max_length=12, blank=True, null=True, verbose_name='中心城市')

    class Meta:
        verbose_name = '省级行政区'
        verbose_name_plural = verbose_name
        managed = False
        db_table = 'prov'
