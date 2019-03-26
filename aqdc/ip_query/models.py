# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IpInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    miniip = models.BigIntegerField(unique=True, blank=True, null=True)
    maxip = models.BigIntegerField(blank=True, null=True)
    continent = models.CharField(max_length=16, blank=True, null=True)
    areacode = models.CharField(max_length=4, blank=True, null=True)
    adcode = models.CharField(max_length=10, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    bd_lon = models.CharField(max_length=12, blank=True, null=True)
    bd_lat = models.CharField(max_length=12, blank=True, null=True)
    wgs_lon = models.CharField(max_length=12, blank=True, null=True)
    wgs_lat = models.CharField(max_length=12, blank=True, null=True)
    radius = models.CharField(max_length=10, blank=True, null=True)
    scence = models.CharField(max_length=10, blank=True, null=True)
    accuracy = models.CharField(max_length=10, blank=True, null=True)
    owner = models.CharField(db_column='OWNER', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ip_info'
