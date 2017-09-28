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
        portfolio_value_before = portfolio_value
        portfolio_value_after = portfolio_value + profit
        profit_percent = profit / portfolio_value_before * 100
        trades.loc[index, 'position_size'] = position_size
        trades.loc[index, 'profit'] = profit
        trades.loc[index, 'profit_percent'] = profit_percent
        trades.loc[index, 'portfolio_value_before'] = portfolio_value_before
        trades.loc[index, 'portfolio_value_after'] = portfolio_value_after
        portfolio_value = portfolio_value_after

    return trades
