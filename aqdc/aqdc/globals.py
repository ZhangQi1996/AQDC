"""
    以下均为全局的变量，应当注意多线程安全问题
"""
import time
from threading import Lock
from rest_framework.response import Response
from rest_framework import status
from app.models import *
from django.conf import settings

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

# **********************************************************************************

def global_cache_time_interval_timeout(time_interval=3600):
    """
    测试当前调用本函数跟global_cache中的last_time时间间隔是否大于time_interval
    是返回True，否则返回False
    :param time_interval: 时间间隔，默认是一小时
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
                print("ok...")
                global_err['err'] = True
                break


def check_update_cur_data():
    """
    检测缓存并更新
    :return: True表示已经跟新
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
