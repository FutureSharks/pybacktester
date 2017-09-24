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

    # Close last position
    price_data.iloc[-1, price_data.columns.get_loc('position')] = 0

    # Create position groups
    price_data['position_group'] = (price_data['position'].diff(1) != 0).astype('int').cumsum()
    price_data['position_group_day_after'] = price_data['position_group'].shift(1)

    return price_data
