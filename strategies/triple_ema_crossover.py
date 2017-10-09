# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def apply(price_data, slow_ema=50, medium_ema=25, fast_ema=10):
    '''
    Triple EMA crossover
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

    return price_data
