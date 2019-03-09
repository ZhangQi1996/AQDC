# xadmin

import xadmin
from .models import *

from django.forms import Widget
@xadmin.sites.register(xadmin.views.BaseAdminView)
class BaseSetting(object):
    enable_themes = True   # 开启主题使用
    use_bootswatch = True  # 开启主题选择


@xadmin.sites.register(xadmin.views.CommAdminView)
class GlobalSettings(object):
    site_title = '后台管理系统' # 修改页眉
    # 若你要修改xadmin中页脚的显示请修改xadmin / templates / xadmin / base_site.html中的内容
    # site_footer = 'Powered By Infinity Group'  # 修改页脚
    menu_style = 'accordion'  #修改菜单栏 改成收缩样式


@xadmin.sites.register(AqiInfo)
class AqiInfoAdmin(object):
    pass


@xadmin.sites.register(Prov)
class ProvAdmin(object):
    pass


@xadmin.sites.register(CityProv)
class CityProvAdmin(object):
    pass


@xadmin.sites.register(CurData)
class CurDataAdmin(object):
    pass

