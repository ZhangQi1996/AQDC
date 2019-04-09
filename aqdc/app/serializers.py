# This is an auto-generated Django-REST-FRAMEWORK serializer module that based upon mysql.
from .models import AqiInfo, CityProv, Prov, CurData
from rest_framework import serializers


class AqiInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = AqiInfo
		fields = ('city_code', 'date', 'pri_pollutant', 'aqi')


class CityProvSerializer(serializers.ModelSerializer):
	class Meta:
		model = CityProv
		fields = ('city_code', 'city_name', 'prov_name', 'longitude', 'latitude')


class ProvSerializer(serializers.ModelSerializer):
	class Meta:
		model = Prov
		fields = ('prov_name', 'prov_cap')


class CurDataSerializer(serializers.ModelSerializer):
	class Meta:
		model = CurData
		fields = ('city_code', 'time', 'aqi', 'pm2_5', 'pm10', 'so2', 'no2', 'co', 'o3', 'pri_pollutant',)
