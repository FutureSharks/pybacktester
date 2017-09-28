# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import itertools
import gc

from .generate_trades import generate_trades
from .simulate_trades import simulate_trades
from .get_backtest_statistics import get_backtest_statistics


def run_backtest(position_data, portfolio_value, position_percentage, stop_pips, spread_pips, slippage_pips=0.0):
    '''
    Takes price data with position column, runs backtest and returns dictionary
    of stats, results dataframe and trades dataframe
    '''
    begin_portfolio_value = portfolio_value

    trades = generate_trades(position_data, stop_pips=stop_pips, spread_pips=spread_pips, slippage_pips=slippage_pips)

    if len(trades) == 0:
        print('no trades generated')
        return (None, None, None)

    simulated_trades = simulate_trades(trades, portfolio_value, position_percentage)

    try:
        wins = simulated_trades['profitable'].value_counts()[1]
    except KeyError:
        wins = 0

    stats = get_backtest_statistics(simulated_trades)

    columns = stats.keys()
    results = pd.DataFrame(columns=columns)
    results = results.append(stats, ignore_index=True)

    return (stats, results, simulated_trades)



def run_backtest_matrix(strategy, position_data, strategy_settings, stop_pips=3, spread_pips=1.3, slippage_pips=1.6):
    '''
    Runs a backtest with multiple settings and returns from results generated trades in a dataframe
    '''

    backtest_results = pd.DataFrame()

    strategy_settings_keys = list(strategy_settings.keys())
    backtest_permutations = []
    for setting in strategy_settings_keys:
        backtest_permutations.append(strategy_settings[setting])

    backtest_settings_list = list(itertools.product(*backtest_permutations))
    number_of_permutations = len(backtest_settings_list)
    permutations_done = 0

    print('Starting, {0} permutations to run.'.format(number_of_permutations))

    for backtest_setting in backtest_settings_list:
        gc.collect()
        settings_dict = dict(zip(strategy_settings_keys, backtest_setting))
        positions = strategy.apply(position_data.copy(), **settings_dict)
        permutations_done += 1

        if positions['position'].value_counts()[0] == len(positions):
            print('Skipped, no trades: {0}/{1}: {2}'.format(permutations_done, number_of_permutations, back_results_dict))
            continue

        trades = generate_trades(positions, stop_pips=stop_pips, spread_pips=spread_pips, slippage_pips=slippage_pips)

        try:
            wins = trades['profitable'].value_counts()[1]
        except KeyError:
            wins = 0

        stats = {
            'win_loss_ratio': wins / len(trades),
            'trades': len(trades),
            'total_pips': trades['pips'].sum(),
            'pips_per_trade': trades['pips'].sum() / len(trades),
            'median_position_length': trades['position_length'].median(),
        }

        back_results_dict = {**stats, **settings_dict}
        backtest_results = backtest_results.append(back_results_dict, ignore_index=True)
        # Try del statement here
        print('{0}/{1}: {2}'.format(permutations_done, number_of_permutations, back_results_dict))

    return backtest_results
