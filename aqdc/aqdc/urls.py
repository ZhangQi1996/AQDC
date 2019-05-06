"""aqdc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include
from django.conf import settings
import xadmin
xadmin.autodiscover()

from xadmin.plugins import xversion
xversion.register_models()

urlpatterns = [
    path(settings.VERSION + 'xadmin/', xadmin.site.urls),
    path(settings.VERSION + 'app/', include('app.urls')),
    path(settings.VERSION + 'ip_query/', include('ip_query.urls')),
    path(settings.VERSION + 'aq_pred/', include('aq_pred.urls')),
]
from django.conf import settings
from django.conf.urls import url
from django.views import static
if settings.DEBUG is False:
    urlpatterns.append(url(r'^static/(?P<path>.*)$', static.serve,
      {'document_root': settings.STATIC_ROOT}, name='static'))
