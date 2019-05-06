"""
    以下均为全局的变量，应当注意多线程安全问题
"""
import time
from threading import Lock
from rest_framework.response import Response
from rest_framework import status
from app.models import *
from django.conf import settings
import numpy as np
from keras.models import Model
from aq_pred.model import get_model
from aq_pred.utils import get_rlv_params, get_aqi_and_combine
from aq_pred.predict import predict
import keras.backend as K

# **********************************************************************************

"""
全局变量：global_cache
    - 用于缓存全国空气质量数据
    - 当调用API获取该数据时，若当时时间与上一时间间隔在规定内
    - 在直接返回cache中的数据
    - 反之，则先爬取目标数据重置cache与last_time，并返回
"""
global_cache = {
    'last_time': 0,
    'cur_data': None,
    'lock': Lock(),
}

global_err = {
    'err': False,
    'lock': Lock(),
}

global_city_code_to_city_name_map = {
    'map': None,
    'lock': Lock(),
}

global_aq_pred_data = {
    'last_time': 0,
    'zz_past_28': None,
    'xx_past_7': None,
    'ly_past_7': None,
    'xc_past_7': None,
    'zz_future_pred_4': None,
    'zz_past_pred_4': None,
    'model': None,
    'lock': Lock(),
}

# **********************************************************************************

def global_cache_time_interval_timeout(time_interval=600):
    """
    测试当前调用本函数跟global_cache中的last_time时间间隔是否大于time_interval
    是返回True，否则返回False
    :param time_interval: 时间间隔，默认是10分钟
    :return: boolean
    """
    if time.time() - global_cache.get('last_time') > time_interval:
        return True
    else:
        return False


def global_cache_get_last_time():
    return global_cache.get('last_time')


def global_cache_set_last_time(last_time=time.time()):
    global_cache['last_time'] = last_time


def global_cache_get_cur_data():
    return global_cache.get('cur_data')


def global_cache_set_cur_data(cur_data: list):
    global_cache['cur_data'] = cur_data


def global_cache_acquire(blocking=True, timeout=-1):
    """
    获取global_cache的锁
    :param timeout: 设置获取锁的
    :return:
    """
    return global_cache['lock'].acquire(blocking=blocking, timeout=timeout)


def global_cache_release():
    """
    释放global_cache的锁
    :return:
    """
    global_cache['lock'].release()


def global_city_code_to_city_name_map_acquire(blocking=True, timeout=-1):
    """
    获取global_city_code_to_city_name_map的锁
    :param timeout: 设置获取锁的
    :return:
    """
    return global_city_code_to_city_name_map['lock'].acquire(blocking=blocking, timeout=timeout)


def global_city_code_to_city_name_map_release():
    """
    释放global_city_code_to_city_name_map的锁
    :return:
    """
    global_city_code_to_city_name_map['lock'].release()


def global_aq_pred_data_interval_timeout(time_interval=600):
    """
    测试当前调用本函数跟global_aq_pred_data中的last_time时间间隔是否大于time_interval
    是返回True，否则返回False
    :param time_interval: 时间间隔，默认是10分钟
    :return: boolean
    """
    if time.time() - global_aq_pred_data.get('last_time') > time_interval:
        return True
    else:
        return False


def global_aq_pred_data_get_last_time():
    return global_aq_pred_data.get('last_time')


def global_aq_pred_data_set_last_time(last_time=time.time()):
    global_aq_pred_data['last_time'] = last_time


def global_aq_pred_data_get_zz_past_28():
    return global_aq_pred_data.get('zz_past_28')


def global_aq_pred_data_set_zz_past_28(zz_past_28):
    global_aq_pred_data['zz_past_28'] = zz_past_28


def global_aq_pred_data_get_xx_past_7():
    return global_aq_pred_data.get('xx_past_7')


def global_aq_pred_data_set_xx_past_7(xx_past_7):
    global_aq_pred_data['xx_past_7'] = xx_past_7


def global_aq_pred_data_get_ly_past_7():
    return global_aq_pred_data.get('ly_past_7')


def global_aq_pred_data_set_ly_past_7(ly_past_7):
    global_aq_pred_data['ly_past_7'] = ly_past_7


def global_aq_pred_data_get_xc_past_7():
    return global_aq_pred_data.get('xc_past_7')


def global_aq_pred_data_set_xc_past_7(xc_past_7):
    global_aq_pred_data['xc_past_7'] = xc_past_7


def global_aq_pred_data_get_zz_future_pred_4():
    return global_aq_pred_data.get('zz_future_pred_4')


def global_aq_pred_data_set_zz_future_pred_4(zz_future_pred_4):
    global_aq_pred_data['zz_future_pred_4'] = zz_future_pred_4


def global_aq_pred_data_get_zz_past_pred_4():
    return global_aq_pred_data.get('zz_past_pred_4')


def global_aq_pred_data_set_zz_past_pred_4(zz_past_pred_4):
    global_aq_pred_data['zz_past_pred_4'] = zz_past_pred_4


def global_aq_pred_data_get_model():
    return global_aq_pred_data.get('model')


def global_aq_pred_data_set_model(model: Model):
    global_aq_pred_data['model'] = model


def global_aq_pred_data_acquire(blocking=True, timeout=-1):
    """
    global_aq_pred_data
    :param timeout: 设置获取锁的
    :return:
    """
    return global_aq_pred_data['lock'].acquire(blocking=blocking, timeout=timeout)


def global_aq_pred_data_release():
    """
    global_aq_pred_data锁的释放
    :return:
    """
    global_aq_pred_data['lock'].release()

# ***********************************************************


def send_bug_email(err: Exception):
    from django.core import mail
    conn = mail.get_connection()
    conn.open()
    subject = u"啊欧~~，你的程序GG了..."
    body = """<html>
                    <body>
                        <h3><i style='color:#349CFF;'>【Infinity Group: BUG侦测系统】</i></h3>
                        <p>
                            <strong>助手小i提醒您</strong>  位于
                            <font color='green'>
                                <a href='https://www.aliyun.com/'>腾讯云服务器</a>
                            </font>上基于Django的web程序已经GG了，
                            <font color='red'>请赶快前往抢修BUG！！！</font>
                        </p>
                        <h4><font color='red'>TRACEBACK:</font></h4>
                        <p><font color='red'>%s</font></p>
                        <p><font color='red'>%s</font></p>
                    </body>
                  </html>
                """ % (err.__str__(), '出错类型：' + str(err.__class__).lstrip('<').rstrip('>'))
    email = mail.EmailMessage(
        subject,
        body,
        '18239961260@163.com',
        ["358929931@qq.com", "1424851327@qq.com"],
        connection=conn,
    )
    email.content_subtype = "html"
    email.send()
    conn.close()
    pass


def global_err_addr(e):
    """全局异常处理"""
    if global_err['err'] is True:
        print(e)
    else:
        while True:
            if global_err['lock'].acquire():
                send_bug_email(e)
                global_err['lock'].release()
                global_err['err'] = True
                break


def check_update_cur_data():
    """
    检测缓存并更新
    :return: True表示已经跟新
    warning：所有加锁情况均为写锁，没有读锁，可能存在写时读的异常状态
    """
    if global_cache_time_interval_timeout():
        # 超时
        data = CurData.objects.filter(city_code__startswith='41').order_by('-time')  # 获得所有河南的数据
        time_ = data[0].time
        cur_data = CurData.objects.filter(time=time_)  # 获取最新的全国数据
        while True:
            if global_cache_acquire():  # 获得缓存锁
                global_cache_set_cur_data(cur_data=cur_data)  # 更新缓存
                global_cache_set_last_time()  # 重置当前时间
                global_cache_release()  # 释放缓存锁
                return True
    return False


def catch_exception(func):
    """用于Views的返回,捕获异常发送邮件"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if settings.DEBUG is False:
                global_err_addr(e)
            return Response({"detail": "内部错误"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return wrapper


def get_global_city_code_to_city_name_map():
    while global_city_code_to_city_name_map['map'] is None:
        if global_city_code_to_city_name_map_acquire():  # 获得global_city_code_to_city_name_map锁
            map = {}
            res = CityProv.objects.all()
            for city_prov in res:
                map[city_prov.city_code] = city_prov.city_name
            global_city_code_to_city_name_map['map'] = map
            global_city_code_to_city_name_map_release()  # 释放global_city_code_to_city_name_map锁
    return global_city_code_to_city_name_map['map']


def check_update_aq_pred_data():
    """
    检测aq_pred_data缓存并更新
    :return: True表示已经跟新
    warning：所有加锁情况均为写锁，没有读锁，可能存在写时读的异常状态
    """
    if global_aq_pred_data_interval_timeout():
        if global_aq_pred_data_get_model() is None:     # 加锁进行配置模型
            while True:  # 更改model时加锁
                if global_aq_pred_data_acquire():  # 获得缓存锁
                    K.clear_session()
                    global_aq_pred_data_set_model(get_model())  # 加载已经训练好的模型
                    global_aq_pred_data_release()
                break
        # 超时
        zz_past_28 = list(CurData.objects.raw("SELECT * FROM cur_data WHERE city_code=%s AND "
                                         "TIME > DATE_SUB(NOW(),INTERVAL %s HOUR)" % (410100, 30)))
        if len(zz_past_28) >= 28:
            zz_past_28 = zz_past_28[len(zz_past_28) - 28:]
        xx_past_7 = list(CurData.objects.raw("SELECT * FROM cur_data WHERE city_code=%s AND "
                                        "TIME > DATE_SUB(NOW(),INTERVAL %s HOUR)" % (410700, 9)))
        if len(xx_past_7) >= 7:
            xx_past_7 = xx_past_7[len(xx_past_7) - 7:]
        ly_past_7 = list(CurData.objects.raw("SELECT * FROM cur_data WHERE city_code=%s AND "
                                        "TIME > DATE_SUB(NOW(),INTERVAL %s HOUR)" % (410300, 9)))
        if len(ly_past_7) >= 7:
            ly_past_7 = ly_past_7[len(ly_past_7) - 7:]
        xc_past_7 = list(CurData.objects.raw("SELECT * FROM cur_data WHERE city_code=%s AND "
                                        "TIME > DATE_SUB(NOW(),INTERVAL %s HOUR)" % (411000, 9)))
        if len(xc_past_7) >= 7:
            xc_past_7 = xc_past_7[len(xc_past_7) - 7:]

        def aq_pred_data_handler(data, hours):
            _ = np.zeros((hours, 6))
            for i, item in enumerate(data):
                _[i][0] = item.pm2_5
                _[i][1] = item.pm10
                _[i][2] = item.so2
                _[i][3] = item.no2
                _[i][4] = item.co
                _[i][5] = item.o3
            return _

        x_params_list, y_params = get_rlv_params()
        model = global_aq_pred_data_get_model()

        x = []
        x.append(aq_pred_data_handler(zz_past_28[:24], 24))
        x.append(aq_pred_data_handler(xx_past_7[:3], 3))
        x.append(aq_pred_data_handler(ly_past_7[:3], 3))
        x.append(aq_pred_data_handler(xc_past_7[:3], 3))
        x.append(np.zeros((4, 6)))
        zz_past_pred_4 = predict(model=model, x=x, x_params_list=x_params_list, y_params=y_params, is_many=False)
        zz_past_pred_4 = get_aqi_and_combine(zz_past_pred_4)
        # 将np.ndarray的zz_past_pred_4 ==> dict list
        _ = []
        t = int(time.mktime(xx_past_7[2].time.timetuple()))
        for i, h in enumerate(zz_past_pred_4):
            t += 3600
            obj = CurData()
            obj.city_code = '410100'
            obj.time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t))
            obj.aqi = h[0]
            obj.pm2_5 = h[1]
            obj.pm10 = h[2]
            obj.so2 = h[3]
            obj.no2 = h[4]
            obj.co = h[5]
            obj.o3 = h[6]
            obj.pri_pollutant = '预测暂不支持首要污染物'
            _.append(obj)
        zz_past_pred_4 = _

        x = []
        x.append(aq_pred_data_handler(zz_past_28[4:], 24))
        x.append(aq_pred_data_handler(xx_past_7[4:], 3))
        x.append(aq_pred_data_handler(ly_past_7[4:], 3))
        x.append(aq_pred_data_handler(xc_past_7[4:], 3))
        x.append(np.zeros((4, 6)))
        zz_future_pred_4 = predict(model=model, x=x, x_params_list=x_params_list, y_params=y_params, is_many=False)
        zz_future_pred_4 = get_aqi_and_combine(zz_future_pred_4)
        # 将np.ndarray的zz_future_pred_4 ==> dict list
        _ = []
        t = int(time.mktime(xx_past_7[-1].time.timetuple()))
        for i, h in enumerate(zz_future_pred_4):
            t += 3600
            obj = CurData()
            obj.city_code = '410100'
            obj.time = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(t))
            obj.aqi = h[0]
            obj.pm2_5 = h[1]
            obj.pm10 = h[2]
            obj.so2 = h[3]
            obj.no2 = h[4]
            obj.co = h[5]
            obj.o3 = h[6]
            obj.pri_pollutant = '预测暂不支持首要污染物'
            _.append(obj)
        zz_future_pred_4 = _
        while True:
            if global_aq_pred_data_acquire():  # 获得锁
                global_aq_pred_data_set_zz_past_28(zz_past_28)
                global_aq_pred_data_set_xx_past_7(xx_past_7)
                global_aq_pred_data_set_ly_past_7(ly_past_7)
                global_aq_pred_data_set_xc_past_7(xc_past_7)
                global_aq_pred_data_set_zz_future_pred_4(zz_future_pred_4)
                global_aq_pred_data_set_zz_past_pred_4(zz_past_pred_4)
                global_aq_pred_data_set_last_time()  # 重置当前时间
                global_aq_pred_data_release()  # 释放锁
                return True
    return False
