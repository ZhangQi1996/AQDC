import numpy as np
from math import ceil

DATA_TYPE = 'float32'

MODEL_WEIGHTS_FILE_PATH = 'aq_pred/model_weights.h5'

X_PARAMS_LIST_FILE_PATH = 'aq_pred/x_params_list.txt'

Y_PARAMS_FILE_PATH = 'aq_pred/y_params.txt'

# 1h
AQI_RULER = [
    [0, 35, 75, 115, 150, 250, 350, 500],   # pm2.5
    [0, 50, 150, 250, 350, 420, 500, 600],  # pm10
    [0, 150, 500, 650, 800],    # so2
    [0, 100, 200, 700, 1200, 2340, 3090, 3840],     # no2
    [0, 5, 10, 35, 60, 90, 120, 150],   # co
    [0, 100, 160, 215, 265, 800]    # o3
]

IAQI_RULER = [0, 50, 100, 150, 200, 300, 400, 500]


def _standardize(array, params=None, return_params=True):
    """
    调整每个属性到X~N(0, sigma)
    x' = (x - mu) / sigma
    :param array:
    :param params: (mu, sigma)
    :return: array_stded, mu, sigma
    """
    if array.ndim not in (2, 3):
        raise TypeError('当前正则化只支持2维或3维')
    if array.ndim == 3:
        x, y, z = array.shape
        _array = array.reshape((x * y, z))
        if params is None:
            mu = np.mean(_array, axis=0)
            sigma = np.sqrt(np.var(_array, axis=0))
        else:
            mu, sigma = params
        if mu.all() != 0 or sigma.all() != 0:
            _array_stded = (_array - mu) / sigma
            array_stded = _array_stded.reshape((x, y, z))
        else:
            array_stded = np.zeros((x, y, z))
    else:
        if params is None:
            mu = np.mean(array, axis=0)
            sigma = np.sqrt(np.var(array, axis=0))
        else:
            mu, sigma = params
        if mu.all() != 0 or sigma.all() != 0:
            array_stded = (array - mu) / sigma
        else:
            array_stded = np.zeros(array.shape)
    if return_params:
        return array_stded, (mu, sigma)
    else:
        return array_stded


def standardize(x, params_list=None, return_params_list=True):
    """将x标准化，其中x = [zz_inputs, xx_inputs, ly_inputs, xc_inputs, decoder_inputs]"""
    x_stded = []
    if params_list is not None:
        for i in range(len(x)):
            x_stded.append(_standardize(x[i], params=params_list[i], return_params=True)[0])
    else:
        params_list = []
        for i in range(len(x)):
            _ = _standardize(x[i], params=None, return_params=True)
            x_stded.append(_[0])
            params_list.append(_[1])
    if return_params_list:
        return x_stded, params_list
    else:
        return x_stded


def inverse_std(array_stded, params):
    """将已经标准化过的数组逆标准化，支持1~3维数据，常见x, y"""
    mu, sigma = params
    if array_stded.ndim < 3:
        return array_stded * sigma + mu
    elif array_stded.ndim == 3:
        x, y, z = array_stded.shape
        array = array_stded.reshape((x * y, z)) * sigma + mu
        return array.reshape((x, y, z))
    else:
        raise TypeError('不支持大于3维的数组逆标准化..')


def load_std_params_list_or_params(file_name, encoding='utf-8', is_params_list=True):
    params_list = []
    with open(file=file_name, mode='r', encoding=encoding) as f:
        while f.readable():
            line = f.readline()
            if line == '':
                break
            mu, sigma = line.rstrip('\n').split('#')
            mu = np.array([float(_) for _ in mu.split(' ')])
            sigma = np.array([float(_) for _ in sigma.split(' ')])
            params_list.append((mu, sigma))
    if is_params_list:
        return params_list
    else:
        return params_list[0]


def get_rlv_params(f1=X_PARAMS_LIST_FILE_PATH, f2=Y_PARAMS_FILE_PATH):
    """获得相关参数"""
    return load_std_params_list_or_params(file_name=f1, is_params_list=True), \
           load_std_params_list_or_params(file_name=f2, is_params_list=False)


def _cpt_iaqi(cp, bph, bpl, iaqih, iaqil):
    """计算某一项目的IAQI值"""
    return (iaqih - iaqil) * (cp - bpl) / (bph - bpl) + iaqil


def _get_low_and_high(ruler, cp):
    """在ruler中计算其bp, iaqi下限值与上限值，当超过最大上限值时，返回的上限值就是cp值"""
    i, l, bpl, bph, iaqil, iaqih = 1, len(ruler), 0, 0, 0, 0
    while i < l:
        if cp < ruler[i]:
            bpl = ruler[i-1]
            bph = ruler[i]
            iaqil = IAQI_RULER[i-1]
            iaqih = IAQI_RULER[i]
            break
        i += 1
    if i >= l:
        bpl, bph = ruler[-1], cp
        iaqil = IAQI_RULER[-1]
        iaqih = iaqil + 100
    return bpl, bph, iaqil, iaqih


def _get_one_record_aqi(vec):
    """
    获取一条记录的AQI值
    :param vec:  [PM2.5,PM10,SO2,NO2,CO,O3]
    :return: AQI
    """
    aqi = 0
    for i, cp in enumerate(vec):
        bpl, bph, iaqil, iaqih = _get_low_and_high(AQI_RULER[i], cp)
        _ = _cpt_iaqi(cp, bph, bpl, iaqih, iaqil)
        if _ > aqi:
            aqi = _
    return aqi


def get_aqi_and_combine(array):
    """
    array = (simples, features) or (features)

    """
    if array.ndim not in (1, 2):
        raise TypeError('array必须是一维或二维数据...')
    if array.ndim == 1:
        return np.append((ceil(_get_one_record_aqi(array)), array))
    x, y = array.shape
    y += 1
    aqis = np.array([])
    for vec in array:
        aqis = np.append(aqis, _get_one_record_aqi(vec))
    aqis = aqis.reshape((len(aqis), 1))
    aqis = np.ceil(aqis)
    return np.column_stack((aqis, array))
