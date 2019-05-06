from aqdc.globals import *
from app.serializers import CurDataSerializer
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse


@require_http_methods(['GET'])
@catch_exception
def get_zz_aq_pred(req):
    """获取郑州地区的空气预测
    :returns
    1.郑州过去28h的AQ, 新乡过去7h的AQ，洛阳过去7h的AQ，许昌过去7h的AQ
    2.预测：郑州未来4h的AQ, 郑州过去4h的AQ
    """
    check_update_aq_pred_data()     # 检查
    zz_past_28 = global_aq_pred_data_get_zz_past_28()
    xx_past_7 = global_aq_pred_data_get_xx_past_7()
    ly_past_7 = global_aq_pred_data_get_ly_past_7()
    xc_past_7 = global_aq_pred_data_get_xc_past_7()
    zz_future_pred_4 = global_aq_pred_data_get_zz_future_pred_4()
    zz_past_pred_4 = global_aq_pred_data_get_zz_past_pred_4()
    ret = {}
    ret['zz_past_28'] = CurDataSerializer(zz_past_28, many=True).data
    ret['xx_past_7'] = CurDataSerializer(xx_past_7, many=True).data
    ret['ly_past_7'] = CurDataSerializer(ly_past_7, many=True).data
    ret['xc_past_7'] = CurDataSerializer(xc_past_7, many=True).data
    ret['zz_future_pred_4'] = CurDataSerializer(zz_future_pred_4, many=True).data
    ret['zz_past_pred_4'] = CurDataSerializer(zz_past_pred_4, many=True).data
    return JsonResponse(ret, safe=False, json_dumps_params={'ensure_ascii': False})