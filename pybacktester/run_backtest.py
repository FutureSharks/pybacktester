# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import itertools

from .generate_trades import generate_trades
from .simulate_trades import simulate_trades


def run_backtest(price_data, portfolio_value, position_percentage, stop_pips, spread_pips, slippage_pips=0.0):
    '''
    Takes price data with position column, runs backtest and returns dictionary
    of stats, results dataframe and trades dataframe
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



def run_backtest_matrix(strategy, month_data, strategy_settings, portfolio_value=10000, position_percentage=2, stop_pips=3, spread_pips=1.3, slippage_pips=1.6):
    '''
    Runs a backtest with multiple settings over multiple months and returns average of results into a combined dataframe
    '''

    backtest_results = pd.DataFrame()

    strategy_settings_keys = list(strategy_settings.keys())
    backtest_permutations = []
    for setting in strategy_settings_keys:
        backtest_permutations.append(strategy_settings[setting])

    backtest_settings_list = list(itertools.product(*backtest_permutations))
    number_of_permutations = len(backtest_settings_list) * len(month_data)
    count_of_permutations = 0

    print('Starting, {0} permutations to run.'.format(number_of_permutations))

    for backtest_setting in backtest_settings_list:
        settings_dict = dict(zip(strategy_settings_keys, backtest_setting))
        for month in month_data:
            positions = strategy.apply(month.copy(), **settings_dict)

            if positions['position'].value_counts()[0] == len(positions):
                continue

            stats, results, trades = run_backtest(
                positions.copy(),
                portfolio_value=portfolio_value,
                position_percentage=position_percentage,
                stop_pips=stop_pips,
                spread_pips=spread_pips,
                slippage_pips=slippage_pips
            )

            back_results_dict = {**stats, **settings_dict}
            back_results_dict['month'] = month.index[0].month
            for key in back_results_dict.keys():
                results.loc[0, key] = back_results_dict[key]
            backtest_results = backtest_results.append(results, ignore_index=True)

            count_of_permutations += 1

            print('{0}/{1}: {2}'.format(count_of_permutations, number_of_permutations, back_results_dict))

    # Create average of results for each month
    grouped_results = backtest_results.groupby(by=strategy_settings_keys).mean()
    grouped_results.reset_index(inplace=True)

    return grouped_results
