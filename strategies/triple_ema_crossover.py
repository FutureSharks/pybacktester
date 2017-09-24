# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def apply(price_data, slow_ema=50, medium_ema=25, fast_ema=10):
    '''
    Tripple EMA crossover
    '''
    # Create fast and slow MAs
    price_data['slow_ema'] = price_data['price'].ewm(span=slow_ema, adjust=False).mean()
    price_data['medium_ema'] = price_data['price'].ewm(span=medium_ema, adjust=False).mean()
    price_data['fast_ema'] = price_data['price'].ewm(span=fast_ema, adjust=False).mean()

    # Create positions
    price_data['position'] = np.where(
        (price_data['fast_ema'] > price_data['medium_ema']) &
        (price_data['fast_ema'] > price_data['slow_ema']),
        1, 0
    )
    price_data['position'] = np.where(
        (price_data['fast_ema'] < price_data['medium_ema']) &
        (price_data['fast_ema'] < price_data['slow_ema']),
        -1, price_data['position']
    )

    # Close last position
    price_data.iloc[-1, price_data.columns.get_loc('position')] = 0

    # Create position groups
    price_data['position_group'] = (price_data['position'].diff(1) != 0).astype('int').cumsum()
    price_data['position_group_day_after'] = price_data['position_group'].shift(1)

    return price_data
