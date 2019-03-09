# This is an auto-generated Django admin module.
from .models import AqiInfo, Prov, CityProv, CurData
from django.contrib import admin
admin.site.site_header = '后台管理'


@admin.register(AqiInfo)
class AqiInfoAdmin(admin.ModelAdmin):
	pass


@admin.register(Prov)
class ProvAdmin(admin.ModelAdmin):
	pass


@admin.register(CityProv)
class CityProvAdmin(admin.ModelAdmin):
	pass


@admin.register(CurData)
class CurDataAdmin(admin.ModelAdmin):
	pass


