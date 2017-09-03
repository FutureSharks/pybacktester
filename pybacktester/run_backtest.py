# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from .generate_trades import generate_trades
from .simulate_trades import simulate_trades


def run_backtest(price_data, portfolio_value, position_percentage, stop_pips, spread_pips, slippage_pips=0.0):
    '''
    Takes price data with position column, runs backtest and returns stats and
    results
    '''
    begin_portfolio_value = portfolio_value

    trades = generate_trades(price_data, stop_pips=stop_pips, spread_pips=spread_pips, slippage_pips=slippage_pips)

    if len(trades) == 0:
        print('no trades generated')
        return (None, None)

    trades = simulate_trades(trades, portfolio_value, position_percentage)

    try:
        wins = trades['profitable'].value_counts()[1]
    except KeyError:
        wins = 0

    stats = {
        'position_percentage': position_percentage,
        'win_loss_ratio': wins / len(trades),
        'end_portfolio_value': round(trades['portfolio_value'].tail(1).values[0]),
        'start_portfolio_value': begin_portfolio_value,
        'portfolio_lowest_value': round(trades['portfolio_value'].min()),
        'trades': len(trades),
        'total_pips': trades['pips'].sum(),
        'pips_per_trade': trades['pips'].sum() / len(trades),
        'median_position_length': trades['position_length'].median(),
        'return_percent': round(((trades['portfolio_value'].tail(1).values[0] / begin_portfolio_value) - 1 ) * 100, 2)
    }

    columns = stats.keys()
    results = pd.DataFrame(columns=columns)
    results = results.append(stats, ignore_index=True)

    return (stats, results, trades)
