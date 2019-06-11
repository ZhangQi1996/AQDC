# This is an auto-generated Django-REST-FRAMEWORK views module.
from .serializers import AqiInfoSerializer, CityProvSerializer, ProvSerializer, CurDataSerializer
from rest_framework import generics
from aqdc.globals import *
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q

class AqiInfoList(generics.ListCreateAPIView):
	'''包含request.method: GET-->List查, POST-->增'''
	queryset = AqiInfo.objects.all()
	serializer_class = AqiInfoSerializer

	@catch_exception
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	@catch_exception
	def post(self, request, *args, **kwargs):
		return Response({'details': '暂未开放POST接口'}, status=status.HTTP_403_FORBIDDEN)
		# return self.create(request, *args, **kwargs)

class CityProvList(generics.ListCreateAPIView):
	'''包含request.method: GET-->List查, POST-->增'''
	queryset = CityProv.objects.all()
	serializer_class = CityProvSerializer

	@staticmethod
	@catch_exception
	def _get_all_provs_name():
		return [v for v in Prov.objects.values_list('prov_name', flat=True)]

	@staticmethod
	@catch_exception
	def _get_all_cities_code():
		return [v for v in CityProv.objects.values_list('city_code', flat=True)]

	@staticmethod
	@require_http_methods(['GET'])
	@catch_exception
	def get_all_provs_name(req):
		return JsonResponse(CityProvList._get_all_provs_name(), safe=False, json_dumps_params={'ensure_ascii': False})

	@staticmethod
	@require_http_methods(['GET'])
	@catch_exception
	def get_all_cities_for_certain_prov(req, prov_name):
		"""获取特定省/直辖市下属的所有市级"""
		if prov_name not in CityProvList._get_all_provs_name():
			return JsonResponse({"detail": "未找到。"}, json_dumps_params={'ensure_ascii': False})
		cities = CityProv.objects.filter(prov_name=prov_name)
		ret = {}
		for c in cities:
			ret[str(c.city_code)] = c.city_name
		return JsonResponse(ret, json_dumps_params={'ensure_ascii': False})

	@catch_exception
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	@catch_exception
	def post(self, request, *args, **kwargs):
		return Response({'details': '暂未开放POST接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.create(request, *args, **kwargs)


class ProvList(generics.ListCreateAPIView):
	'''包含request.method: GET-->List查, POST-->增'''
	queryset = Prov.objects.all()
	serializer_class = ProvSerializer

	@catch_exception
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	@catch_exception
	def post(self, request, *args, **kwargs):
		return Response({'details': '暂未开放POST接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.create(request, *args, **kwargs)


class CurDataList(generics.ListCreateAPIView):
	'''包含request.method: GET-->List查, POST-->增'''
	queryset = CurData.objects.all()
	serializer_class = CurDataSerializer

	@catch_exception
	def get(self, request, *args, **kwargs):
		check_update_cur_data()
		# 使用缓存中的数据
		global_cache_reading_acquire()
		cur_data = global_cache_get_cur_data()
		global_cache_reading_release()
		serializer = self.serializer_class(cur_data, many=True)
		return Response(serializer.data)

	@catch_exception
	def post(self, request, *args, **kwargs):
		return Response({'details': '暂未开放POST接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.create(request, *args, **kwargs)

	@staticmethod
	@require_http_methods(['GET'])
	@catch_exception
	def get_relevant_predicted_cities_cur_data(request):
		ret = CurDataList.queryset.filter(Q(city_code=410100) | Q(city_code=410300) |
						Q(city_code=410700) | Q(city_code=411000))
		ret = CurDataSerializer(ret, many=True).data
		return JsonResponse(ret, safe=False, json_dumps_params={'ensure_ascii': False})

class AqiInfoDetail(generics.RetrieveUpdateDestroyAPIView):
	'''包含request.method: GET(pk)-->AqiInfo个体查, PUT-->改, DELETE-->删'''
	queryset = AqiInfo.objects.all()
	serializer_class = AqiInfoSerializer

	@staticmethod
	@require_http_methods(['GET'])
	@catch_exception
	def get_aqi_infos_for_certain_city(request, city_code, days=30):
		"""获取特定城市过去数天的AQI"""
		if city_code not in CityProvList._get_all_cities_code():
			return JsonResponse({"detail": "未找到。"}, json_dumps_params={'ensure_ascii': False})
		aqi_infos = AqiInfo.objects.raw("SELECT * FROM aqi_info  WHERE city_code=%s AND "
										"DATE_SUB(CURDATE(), INTERVAL %s DAY) <= DATE(DATE)" % (city_code, days))
		ret = AqiInfoSerializer(aqi_infos, many=True).data
		return JsonResponse(ret, safe=False, json_dumps_params={'ensure_ascii': False})

	@catch_exception
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	@catch_exception
	def put(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PUT接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.update(request, *args, **kwargs)

	@catch_exception
	def patch(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PATCH接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.partial_update(request, *args, **kwargs)

	@catch_exception
	def delete(self, request, *args, **kwargs):
		return Response({'details': '暂未开放DEL接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.destroy(request, *args, **kwargs)


class CityProvDetail(generics.RetrieveUpdateDestroyAPIView):
	'''包含request.method: GET(pk)-->CityProv个体查, PUT-->改, DELETE-->删'''
	queryset = CityProv.objects.all()
	serializer_class = CityProvSerializer

	@catch_exception
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	@catch_exception
	def put(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PUT接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.update(request, *args, **kwargs)

	@catch_exception
	def patch(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PATCH接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.partial_update(request, *args, **kwargs)

	@catch_exception
	def delete(self, request, *args, **kwargs):
		return Response({'details': '暂未开放DEL接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.destroy(request, *args, **kwargs)


class ProvDetail(generics.RetrieveUpdateDestroyAPIView):
	'''包含request.method: GET(pk)-->Prov个体查, PUT-->改, DELETE-->删'''
	queryset = Prov.objects.all()
	serializer_class = ProvSerializer

	@catch_exception
	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	@catch_exception
	def put(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PUT接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.update(request, *args, **kwargs)

	@catch_exception
	def patch(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PATCH接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.partial_update(request, *args, **kwargs)

	@catch_exception
	def delete(self, request, *args, **kwargs):
		return Response({'details': '暂未开放DEL接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.destroy(request, *args, **kwargs)


class CurDataDetail(generics.RetrieveUpdateDestroyAPIView):
	'''包含request.method: GET(pk)-->Prov个体查, PUT-->改, DELETE-->删'''
	queryset = CurData.objects.all()
	serializer_class = CurDataSerializer

	@staticmethod
	@require_http_methods(['GET'])
	@catch_exception
	def get_all_infos_for_hn_certain_city(req, city_code, hours=24):
		"""获取河南特定城市过去数小时的info"""
		if str(city_code)[:2] != '41':
			return JsonResponse({"detail": "所查找的城市非河南省地区城市。"}, json_dumps_params={'ensure_ascii': False})
		if city_code not in CityProvList._get_all_cities_code():
			return JsonResponse({"detail": "未找到。"}, json_dumps_params={'ensure_ascii': False})
		infos = CurData.objects.raw("SELECT * FROM cur_data WHERE city_code=%s AND "
									"TIME > DATE_SUB(NOW(),INTERVAL %s HOUR)" % (city_code, hours))
		ret = CurDataSerializer(infos, many=True).data
		return JsonResponse(ret, safe=False, json_dumps_params={'ensure_ascii': False})

	@catch_exception
	def get(self, request, *args, **kwargs):
		check_update_cur_data()		# 检查更新缓存
		city_code = kwargs['city_code']
		global_cache_reading_acquire()
		cur_data = global_cache_get_cur_data()
		global_cache_reading_release()
		for item in cur_data:
			if item.city_code == city_code:
				return Response(self.serializer_class(item, many=False).data)
		return Response({"detail": "未找到。"}, status=status.HTTP_404_NOT_FOUND)

	@catch_exception
	def put(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PUT接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.update(request, *args, **kwargs)

	@catch_exception
	def patch(self, request, *args, **kwargs):
		return Response({'details': '暂未开放PATCH接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.partial_update(request, *args, **kwargs)

	@catch_exception
	def delete(self, request, *args, **kwargs):
		return Response({'details': '暂未开放DEL接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.destroy(request, *args, **kwargs)