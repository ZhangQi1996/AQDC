# This is an auto-generated Django-REST-FRAMEWORK serializer module that based upon mysql.
from .models import IpInfo
from rest_framework import serializers


class IpInfoSerializer(serializers.ModelSerializer):
	class Meta:
		model = IpInfo
		fields = ('id ', 'miniip', 'maxip', 'continent', 'areacode', 'adcode',
				'country', 'province', 'city', 'district', 'bd_lon', 'bd_lat',
				'wgs_lon', 'wgs_lat', 'radius', 'scence', 'accuracy', 'owner',)
