import pymysql
'''
    工具模块，可删除
'''

from aqdc.aqdc.settings import DATABASES

# DATABASES = {
#     'default': {
#         'NAME': 'database',
#         'USER': 'account',
#         'PASSWORD': 'pw',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'CHARSET': 'utf-8',
#     }
# }


def addr_class_name(cls_name_iter):
    """
    e.g. ('book', 'aqi_info') --> ('Book', 'AqiInfo')
    :param cls_name_iter:
    :return:
    """
    ret = []
    for cls_name in cls_name_iter:
        if '_' in cls_name:
            cls_ = cls_name.split('_')
            ret.append(''.join([cls.capitalize() for cls in cls_]))
        else:
            ret.append(cls_name.capitalize())
    return ret

def auto_yield_serializers_in_mysql(DATABASES_CONF=DATABASES, encoding = 'utf8'):
    """
    当你使用REST-FRAMEWORK框架，自动生成Serializer类：并在同目录下生成serializers.py文件
    DATABASES_CONF可以使你的django夏目下的settings.py文件中的DATABASES
    :param DATABASES_CONF: {
        'default': {
            'NAME': 'database',
            'USER': 'account',
            'PASSWORD': 'pw',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'CHARSET': 'utf8',
        }
    }
    :return: None
    """
    conn, cur = None, None
    try:
        DATABASES_CONF = DATABASES_CONF['default']
        if 'CHARSET' not in DATABASES_CONF.keys():
            DATABASES_CONF['CHARSET'] = encoding
        if isinstance(DATABASES_CONF['PORT'], str):
            DATABASES_CONF['PORT'] = int(DATABASES_CONF['PORT'])
        conn = pymysql.connect(host=DATABASES_CONF['HOST'], user=DATABASES_CONF['USER'], passwd=DATABASES_CONF['PASSWORD'],
                               db=DATABASES_CONF['NAME'], port=DATABASES_CONF['PORT'],
                               charset=DATABASES_CONF['CHARSET'])
        cur = conn.cursor()
        cur.execute('SHOW TABLES')
        tables_iter = cur.fetchall()
        with open(r'serializers.py', mode='w', encoding=DATABASES_CONF['CHARSET']) as f:
            s = ', '.join(addr_class_name([table_iter[0] for table_iter in tables_iter]))
            f.writelines([
                "# This is an auto-generated Django-REST-FRAMEWORK serializer module that based upon mysql.\n",
                "from .models import %s\n" % s,
                "from rest_framework import serializers\n\n\n",
            ])
            for table_iter in tables_iter:
                cur.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.Columns WHERE table_name='%s' AND table_schema = '%s'" % (
                        table_iter[0], DATABASES_CONF['NAME']))
                attrs_iter = cur.fetchall()
                s = '(' + [attr_iter[0] for attr_iter in attrs_iter].__str__().lstrip('[').rstrip(']') + ')'
                cls_name = addr_class_name((table_iter[0],))[0]
                f.writelines([
                    "class %sSerializer(serializers.ModelSerializer):\n" % cls_name,
                    "\tclass Meta:\n",
                    "\t\tmodel = %s\n" % cls_name,
                    "\t\tfields = %s\n\n\n" % s,
                ])

    except Exception as e:
        print(e)
        raise e
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()


def auto_yield_views_in_DRF(class_list, models_default='.models', serializers_default='.serializers'):
    """
    根据class_list输入的类名可迭代对象，生成符合Django-REST-FRAMEWORK的基于类的views.py文件
    :param class_list: e.g. class_list = ['Book', 'Stu'] or ('Book', 'Stu')
    :param models_default: 从此路径导入models
    :param serializers_default: 从此路径导入serializers
    :return: None
    """
    class_list = addr_class_name(class_list)
    with open(r'views.py', mode='w', encoding='utf-8') as f:
        f.writelines([
            "# This is an auto-generated Django-REST-FRAMEWORK views module.\n",
            "from %s import %s\n" % (models_default, ', '.join(class_list)),
            "from %s import %s\n" % (serializers_default, ', '.join([item + 'Serializer' for item in class_list])),
            "from rest_framework import generics\n\n\n",
        ])
        for cls in class_list:
            f.writelines([
                "class %sList(generics.ListCreateAPIView):\n" % cls,
                "\t'''包含request.method: GET-->List查, POST-->增'''\n",
                "\tqueryset = %s.objects.all()\n" % cls,
                "\tserializer_class = %sSerializer\n\n\n" % cls,
            ])
        for cls in class_list:
            f.writelines([
                "class %sDetail(generics.RetrieveUpdateDestroyAPIView):\n" % cls,
                "\t'''包含request.method: GET(pk)-->%s个体查, PUT-->改, DELETE-->删'''\n" % cls,
                "\tqueryset = %s.objects.all()\n" % cls,
                "\tserializer_class = %sSerializer\n\n\n" % cls,
            ])

if __name__ == '__main__':
    auto_yield_serializers_in_mysql()
