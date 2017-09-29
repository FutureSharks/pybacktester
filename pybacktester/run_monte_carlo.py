# -*- coding: utf-8 -*-


import gc
import pandas as pd
import numpy as np
from itertools import permutations
from .get_backtest_statistics import get_backtest_statistics
from .simulate_trades import simulate_trades


def run_monte_carlo(trades, runs=1000, portfolio_value=10000, position_percentage=1):
    '''
    Takes a list of trades in a dataframe and randomly reorders them and collects statistics.
    This is run repeatedly and agregate statistics are returned.
    '''
    completed_runs = 0
    results = pd.DataFrame()

    print('Running {0} iterations of monte carlo...'.format(runs))

    while completed_runs <= runs:
        # Run garbage collection otherwise pandas uses too much memory
        gc.collect()

        # Randomly reorder trades
        trades = trades.reindex(np.random.permutation(trades.index))
        trades.reset_index(drop=True, inplace=True)

        # Run simulation
        trades = simulate_trades(trades.copy(), portfolio_value=portfolio_value, position_percentage=position_percentage)

        # Get statistics
        stats = get_backtest_statistics(trades)

        # Append to results
        results = results.append(stats, ignore_index=True)

        # Print progress and continue loop
        if completed_runs % 1000 == 0:
            print('{0} completed...'.format(completed_runs))
        completed_runs += 1

    statistics = {
        'drawdown_percent_median': results['drawdown_percent_median'].median(),
        'drawdown_percent_max_median': results['drawdown_percent_max'].median(),
        'profit_factor_median': results['profit_factor'].median(),
        'drawdown_percent_95th_median': results['drawdown_percent_95th'].median()
    }

    return statistics
