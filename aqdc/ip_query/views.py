from rest_framework import generics
from aqdc.globals import *
from .models import IpInfo
from .serializers import IpInfoSerializer
from django.views.decorators.http import require_http_methods
import socket
import struct

class IpInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    '''包含request.method: GET(pk)-->Prov个体查, PUT-->改, DELETE-->删'''
    queryset = IpInfo.objects.all()
    serializer_class = IpInfoSerializer

    @catch_exception
    def get(self, request, *args, **kwargs):
        ip_addr = kwargs['ip_addr']
        if ip_addr in ['localhost', '0.0.0.0', '127.0.0.1']:
            ip_addr = request.META['REMOTE_ADDR']
        ip_num = socket.ntohl(struct.unpack("I", socket.inet_aton(ip_addr))[0])
        infos = IpInfo.objects.raw("select * from ip_info where miniip <= %s order by miniip desc limit 1;" % ip_num)
        if infos is not None:
            for item in infos:
                return Response(IpInfoSerializer(item).data)
        return Response({"detail": "未找到。"}, status=status.HTTP_404_NOT_FOUND)
        return self.get_ip_info(request, ip)

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
