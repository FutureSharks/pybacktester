# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def apply(price_data, slow_ma, fast_ma, bandwidth_pips=0):
    '''
    Dual MA crossover with optional band
    '''
    # Create fast and slow EMAs
    price_data['slow_ma'] = price_data['price'].rolling(window=slow_ma, center=False).mean()
    price_data['fast_ma'] = price_data['price'].rolling(window=fast_ma, center=False).mean()

    # Create band around slow MA
    price_data['slow_ma_high'] = price_data['slow_ma'] + (0.0001 * bandwidth_pips)
    price_data['slow_ma_low'] = price_data['slow_ma'] - (0.0001 * bandwidth_pips)

    # Create positions
    price_data['position'] = np.where(price_data['fast_ma'] > price_data['slow_ma_high'], 1, 0)
    price_data['position'] = np.where(price_data['fast_ma'] < price_data['slow_ma_low'], -1, price_data['position'])

    # Close last position
    price_data.iloc[-1, price_data.columns.get_loc('position')] = 0

    # Create position groups
    price_data['position_group'] = (price_data['position'].diff(1) != 0).astype('int').cumsum()
    price_data['position_group_day_after'] = price_data['position_group'].shift(1)

    return price_data
