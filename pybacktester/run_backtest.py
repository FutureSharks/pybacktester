# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import itertools
import gc

from .generate_trades import generate_trades
from .simulate_trades import simulate_trades
from .get_backtest_statistics import get_backtest_statistics


def run_backtest(position_data, portfolio_value, risk_percentage, stop_pips, spread_pips, slippage_pips=0.0):
    '''
    Takes price data with position column, runs backtest and returns dictionary
    of stats, results dataframe and trades dataframe
    '''
    begin_portfolio_value = portfolio_value

    trades = generate_trades(position_data, stop_pips=stop_pips, spread_pips=spread_pips, slippage_pips=slippage_pips)

    if len(trades) == 0:
        print('no trades generated')
        return (None, None, None)

    simulated_trades = simulate_trades(trades, portfolio_value, risk_percentage)

    try:
        wins = simulated_trades['profitable'].value_counts()[1]
    except KeyError:
        wins = 0

    stats = get_backtest_statistics(simulated_trades)

    columns = stats.keys()
    results = pd.DataFrame(columns=columns)
    results = results.append(stats, ignore_index=True)

    return (stats, results, simulated_trades)
