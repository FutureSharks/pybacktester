# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def apply(price_data, moving_average=10, drop_ma_column=True):
    '''
    Not a strategy for trading or creating positions but just to show trended parts of price data
    '''
    price_data['trend_ma'] = price_data['price'].rolling(window=moving_average).mean()

    # Create trend from moving average
    price_data['position'] = np.where(price_data['trend_ma'] > price_data['trend_ma'].shift(), 1, 0)
    price_data['position'] = np.where(price_data['trend_ma'] < price_data['trend_ma'].shift(), -1, price_data['position'])

    if drop_ma_column:
        price_data.drop('trend_ma', axis=1, inplace=True)

    return price_data
