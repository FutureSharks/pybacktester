# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def apply(price_data, bb_ma=20, bb_std=2, bb_width_threshold=0.008):
    '''
    Bollinger band strategy
    '''
    price_data['bb_ma'] = price_data['price'].rolling(window=bb_ma).mean()
    price_data['bb_std'] = price_data['price'].rolling(window=bb_ma).std()
    price_data['bb_upper'] = price_data['bb_ma'] + (price_data['bb_std'] * bb_std)
    price_data['bb_lower'] = price_data['bb_ma'] - (price_data['bb_std'] * bb_std)
    price_data['bb_width'] = price_data['bb_upper'] - price_data['bb_lower']
    price_data['position'] = np.where(price_data['bb_width'] > bb_width_threshold, 1, 0)

    return price_data
