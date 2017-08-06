# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def apply(price_data, moving_average, bandwidth_pips):
    '''
    Moving average band strategy
    '''
    price_data['ma'] = price_data['price'].rolling(window=moving_average, center=False).mean()
    price_data['ma_high'] = price_data['ma'] + (0.0001 * bandwidth_pips)
    price_data['ma_low'] = price_data['ma'] - (0.0001 * bandwidth_pips)
    price_data['position'] = np.where(price_data['price'] > price_data['ma_high'], 1, 0)
    price_data['position'] = np.where(price_data['price'] < price_data['ma_low'], -1, price_data['position'])

    return price_data
