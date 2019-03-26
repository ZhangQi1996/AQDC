from rest_framework import generics
from aqdc.aqdc.globals import *
from .models import IpInfo
from .serializers import IpInfoSerializer


class IpInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    '''包含request.method: GET(pk)-->Prov个体查, PUT-->改, DELETE-->删'''
    queryset = IpInfo.objects.using('ip_query').all()
    serializer_class = IpInfoSerializer

    @catch_exception
    def get(self, request, *args, **kwargs):
        ip = kwargs['pk']
        infos = IpInfo.objects.using('ip_query')\
            .raw('from ip_info where minip <= INET_ATON(%s) order by minip desc limit 1;' % ip)
        if infos is not None:
            for item in infos:
                return Response(IpInfoSerializer(item))
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
