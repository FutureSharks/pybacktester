# -*- coding: utf-8 -*-

import pandas as pd
import os


basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath, 'data'))


def get(provider, year, month, day=None):
    if day:
        day = "-{0}".format(day)
    else:
        day = ''

    if provider == 'truefx':
        filename = '{0}/truefx/{1}/GBPUSD-{1}-{2}{3}.csv'.format(data_dir, year, month, day)
        price_data = pd.read_csv(filename, names=['pair', 'date', 'low', 'high'])
        price_data['date'] = pd.to_datetime(price_data['date'], infer_datetime_format=True)
        price_data.set_index('date', inplace=True)
        price_data['price'] = (price_data['low'] + price_data['high']) / 2
        for column in ['high', 'low', 'pair']:
            if column in price_data.columns:
                price_data.drop(column, 1, inplace=True)

    elif provider == 'sentdex':
        filename = '{0}/sentdex/{1}/GBPUSD-{1}-{2}{3}.csv'.format(data_dir, year, month, day)
        price_data = pd.read_csv(filename, index_col=0, parse_dates=True, names=['low', 'high'])
        price_data.index.name = 'date'
        price_data['price'] = (price_data['low'] + price_data['high']) / 2

        # Remove duplicate index rows
        price_data = price_data[~price_data.index.duplicated(keep='first')]

        # Remove unused columns
        for column in ['high', 'low']:
            if column in price_data.columns:
                price_data.drop(column, 1, inplace=True)

    else:
        raise Exception

    price_data.dropna(subset=['price'], inplace=True)

    return price_data
