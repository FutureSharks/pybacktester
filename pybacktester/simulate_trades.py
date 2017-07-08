# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def simulate_trades(trades, portfolio_value, position_percentage):
    '''
    Loops through trades, takes a position using a percentage of portfolio
    value and adds columns for each trade, profit and loss
    '''
    for index, row in trades.iterrows():
        position_size = (portfolio_value / 100) * position_percentage
        profit = position_size * row['pips']
        portfolio_value = portfolio_value + profit
        trades.loc[index, 'position_size'] = position_size
        trades.loc[index, 'profit'] = profit
        trades.loc[index, 'portfolio_value'] = portfolio_value

    return trades
