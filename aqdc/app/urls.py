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
from django.urls import path, register_converter
from .registers import CommonConverter
from .views import *


register_converter(CommonConverter, 'common')   # match Chinese, 0-9, -, a-z, A-Z

urlpatterns = [
    path('prov/all/', ProvList.as_view()),
    path('prov/one/<common:pk>/', ProvDetail.as_view()),
    path('city_prov/all/', CityProvList.as_view()),
    path('city_prov/one/<common:pk>/', CityProvDetail.as_view()),
    path('cur_data/all/', CurDataList.as_view()),
    path('cur_data/one/<common:pk>/', CurDataDetail.as_view()),
    path('aqi_info/all/', AqiInfoList.as_view()),
    path('aqi_info/one/<common:pk>/', AqiInfoDetail.as_view()),
    path('cities/<common:prov_name>/', CityProvList.get_all_cities_for_certain_prov),
    path('provs/', CityProvList.get_all_provs_name),
]
