# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def simulate_trades(trades, portfolio_value, risk_percentage):
    '''
    Loops through trades, takes a position using a percentage of portfolio
    value and adds columns for each trade, profit and loss
    '''

    def calculate_position(portfolio_value, risk_percentage, stop_pips):
        '''
        Calculates position size based on amount of portfolio to risk
        '''
        risk_amount = (portfolio_value / 100) * risk_percentage
        position_size = risk_amount / stop_pips
        return position_size

    for index, row in trades.iterrows():
        stop_pips = (row['enter_price'] - row['stop_price']) * row['position'] / 0.0001
        position_size = calculate_position(portfolio_value, risk_percentage, stop_pips)
        profit = position_size * row['pips']
        portfolio_value_before = portfolio_value
        portfolio_value_after = portfolio_value + profit
        profit_percent = profit / portfolio_value_before * 100
        expectancy_1r = (row['enter_price'] - row['stop_price']) * row['position']
        trades.loc[index, 'position_size'] = position_size
        trades.loc[index, 'profit'] = profit
        trades.loc[index, 'profit_percent'] = profit_percent
        trades.loc[index, 'portfolio_value_before'] = portfolio_value_before
        trades.loc[index, 'portfolio_value_after'] = portfolio_value_after
        trades.loc[index, 'expectancy_1r'] = expectancy_1r
        trades.loc[index, 'expectancy_pl'] = (row['exit_price'] - row['enter_price']) / expectancy_1r * row['position']
        portfolio_value = portfolio_value_after

    return trades
