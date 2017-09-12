# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def plot_trades(price_data, trades):
    '''
    Creates a plot of the price with coloured bands to show each trade and outcome
    '''
    for column in price_data.columns:
        if column != 'price':
            price_data.drop(column, 1, inplace=True)

    ax = price_data.plot()
    ymax = price_data['price'].max()
    ymin = price_data['price'].min()

    for index, long_position in trades.loc[trades['profitable'] == True].iterrows():
        enter_loc = price_data.loc[price_data.index == long_position['enter_date']].index[0]
        exit_loc = price_data.loc[price_data.index == long_position['exit_date']].index[0]
        ax.fill_between([enter_loc, exit_loc], ymin, ymax, color='#82ff90')

    for index, short_position in trades.loc[trades['profitable'] == False].iterrows():
        enter_loc = price_data.loc[price_data.index == short_position['enter_date']].index[0]
        exit_loc = price_data.loc[price_data.index == short_position['exit_date']].index[0]
        ax.fill_between([enter_loc, exit_loc], ymin, ymax, color='#ff8282')

    return ax
