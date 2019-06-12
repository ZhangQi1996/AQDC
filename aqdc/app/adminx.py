# xadmin

import xadmin
from .models import *
from aqdc.globals import get_global_city_code_to_city_name_map

@xadmin.sites.register(xadmin.views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True   # 开启主题使用
    use_bootswatch = True  # 开启主题选择


@xadmin.sites.register(xadmin.views.CommAdminView)
class GlobalSettings(object):
    site_title = u'后台管理系统' # 修改页眉
    # 若你要修改xadmin中页脚的显示请修改xadmin / templates / xadmin / base_site.html中的内容
    # site_footer = 'Powered By Infinity Group'  # 修改页脚
    menu_style = 'accordion'  #修改菜单栏 改成收缩样式





# 由于不知道什么原因Prov的管理部分无法展示，找不出bug
# @xadmin.sites.register(Prov)
# class ProvAdmin(object):
#     # list_display = ('prov_name', 'prov_cap')
#     pass


@xadmin.sites.register(CityProv)
class CityProvAdmin(object):
    list_display = ('city_name', 'city_code', 'prov_name', 'longitude', 'latitude')
    search_fields = ['city_name', 'prov_name']


@xadmin.sites.register(CurData)
class CurDataAdmin(object):

    def get_city_name(self, obj):
        map = get_global_city_code_to_city_name_map()
        return map[obj.city_code]

    get_city_name.short_description = u'城市/区域名'
    get_city_name.allow_tags = True
    list_display = ('get_city_name', 'city_code', 'time', 'aqi', 'pm2_5', 'pm10', 'so2', 'no2', 'co', 'o3', 'pri_pollutant',)


@xadmin.sites.register(AqiInfo)
class AqiInfoAdmin(object):
    def get_city_name(self, obj):
        map = get_global_city_code_to_city_name_map()
        return map[obj.city_code]

    get_city_name.short_description = u'城市/区域名'
    get_city_name.allow_tags = True

    list_display = ('get_city_name', 'city_code', 'date', 'aqi', 'pri_pollutant')