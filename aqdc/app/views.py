# This is an auto-generated Django-REST-FRAMEWORK views module.
from .serializers import AqiInfoSerializer, CityProvSerializer, ProvSerializer, CurDataSerializer
from rest_framework import generics
from aqdc.globals import *
from rest_framework.response import Response
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse

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
		cur_data = global_cache_get_cur_data()
		serializer = self.serializer_class(cur_data, many=True)
		return Response(serializer.data)

	@catch_exception
	def post(self, request, *args, **kwargs):
		return Response({'details': '暂未开放POST接口'}, status=status.HTTP_403_FORBIDDEN)
		#
		# return self.create(request, *args, **kwargs)


class AqiInfoDetail(generics.RetrieveUpdateDestroyAPIView):
	'''包含request.method: GET(pk)-->AqiInfo个体查, PUT-->改, DELETE-->删'''
	queryset = AqiInfo.objects.all()
	serializer_class = AqiInfoSerializer

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

	@catch_exception
	def get(self, request, *args, **kwargs):
		check_update_cur_data()		# 检查更新缓存
		city_code = int(kwargs['pk'])
		for item in global_cache_get_cur_data():
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