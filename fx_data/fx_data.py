# -*- coding: utf-8 -*-

import pandas as pd
import os
import glob


basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath, 'data'))


def get(provider, year, month, day=None, time_group=None, instrument=None):
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

    elif provider == 'oanda':
        filename = '{0}/oanda/{1}/{2}/oanda-{1}-{2}-{3}.csv'.format(data_dir, instrument, year, month, day)
        try:
            price_data = pd.read_csv(filename, index_col=0)
        except FileNotFoundError:
            return None
        price_data.index.name = 'date'
        price_data.index = pd.to_datetime(price_data.index)
        price_data['price'] = (price_data['open'] + price_data['close']) / 2
        # Remove duplicate index rows
        price_data = price_data[~price_data.index.duplicated(keep='first')]

    else:
        raise Exception

    if time_group:
        price_data = price_data.groupby(pd.TimeGrouper(freq=time_group)).mean()

    price_data = price_data.dropna(subset=['price'])

    return price_data


def get_all(provider, instrument, year='*', time_group=None):
    if provider == 'oanda':
        price_data = pd.DataFrame()
        csv_files = glob.glob('{0}/oanda/{1}/{2}/*.csv'.format(data_dir, instrument, year))
        for csv_file in csv_files:
            price_data = price_data.append(pd.read_csv(csv_file, index_col=0))
        price_data.index.name = 'date'
        price_data.index = pd.to_datetime(price_data.index)
        price_data['price'] = (price_data['open'] + price_data['close']) / 2
        # Remove duplicate index rows
        price_data = price_data[~price_data.index.duplicated(keep='first')]

    if time_group:
        price_data = price_data.groupby(pd.TimeGrouper(freq=time_group)).mean()

    price_data = price_data.dropna(subset=['price'])

    return price_data
