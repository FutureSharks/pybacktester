# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def get_backtest_statistics(trades):
    '''
    Takes a dataframe of trades and returns a dictionary of statistics
    '''
    if len(trades) == 0:
        return None

    # See if there are columns to calculate extended information
    if 'profit_percent' in trades.columns and 'portfolio_value_before' in trades.columns:
        extended_stats = True
    else:
        extended_stats = False

    # Group series of profitable/non-profitable trades to calculate drawdown
    trades['win_loss_group'] = (trades['profitable'].diff(1) != 0).astype('int').cumsum()

    # Calculate win/loss numbers
    wins = trades[trades.profitable == True]
    losses = trades[trades.profitable == False]

    # If required columns are present then calculate extra information like drawdown etc
    if extended_stats:
        start_portfolio_value = trades['portfolio_value_before'].head(1).values[0]
        end_portfolio_value = trades['portfolio_value_after'].tail(1).values[0]
        # Calculate drawdown information
        draw_downs = pd.DataFrame({
            'from': losses.reset_index().groupby('win_loss_group')['enter_date'].first(),
            'to': losses.reset_index().groupby('win_loss_group')['exit_date'].last(),
            'length': losses.reset_index().groupby('win_loss_group')['position_length'].sum(),
            'portfolio_value_before': losses.reset_index().groupby('win_loss_group')['portfolio_value_before'].first(),
            'portfolio_value_after': losses.reset_index().groupby('win_loss_group')['portfolio_value_after'].last(),
        })
        draw_downs['loss'] = draw_downs['portfolio_value_before'] - draw_downs['portfolio_value_after']
        draw_downs['loss_percent'] = draw_downs['loss'] / draw_downs['portfolio_value_before'] * 100
        trades.drop('win_loss_group', 1, inplace=True)

    # Get trading time span in days
    numpy_td = trades['exit_date'].tail(1).values[0] - trades['enter_date'].head(1).values[0]
    days = numpy_td.astype('timedelta64[D]')
    trading_days = max(days / np.timedelta64(1, 'D'), 1)

    # Create the statistics dictionary
    statistics = {
        'win_loss_ratio': len(wins) / len(trades),
        'trades': len(trades),
        'trades_per_day': len(trades) / trading_days,
        'total_pips': trades['pips'].sum(),
        'pips_per_win_trade': wins['pips'].mean(),
        'pips_per_loss_trade': losses['pips'].mean(),
        'win_length_median': wins['position_length'].median(),
        'loss_length_median': losses['position_length'].median(),
        'pip_profit_factor': wins['pips'].sum() / max((losses['pips'].sum() * -1), 1),
    }

    if extended_stats:
        ext_stats = {
            'start_portfolio_value': start_portfolio_value,
            'end_portfolio_value': end_portfolio_value,
            'return_percent': (end_portfolio_value - start_portfolio_value) / start_portfolio_value * 100,
            'portfolio_lowest_value': min([trades['portfolio_value_after'].min(), trades['portfolio_value_before'].min()]),
            'win_percent_median': wins['profit_percent'].median(),
            'drawdown_percent_max': draw_downs['loss_percent'].max(),
            'drawdown_percent_median': draw_downs['loss_percent'].median(),
            'drawdown_percent_95th': draw_downs['loss_percent'].quantile(0.95),
            'profit_factor': wins['profit'].sum() / max((losses['profit'].sum() * -1), 1),
        }
        statistics = {**statistics, **ext_stats }

    return statistics
