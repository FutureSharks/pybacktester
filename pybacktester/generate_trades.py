# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def generate_trades(price_data, stop_pips=None):
    '''
    Takes price_data with poition column and returns a list of trades with
    enter/exit dates and enter/exit prices
    '''
    # Close last position
    price_data.iloc[-1, price_data.columns.get_loc('position')] = 0

    # Create position groups
    price_data['position_group'] = (price_data['position'].diff(1) != 0).astype('int').cumsum()
    price_data['position_group_day_after'] = price_data['position_group'].shift(1)

    # Create trades DataFrame
    trades = pd.DataFrame({
            'enter_date' : price_data.reset_index().groupby('position_group').date.first(),
            'enter_price' : price_data.reset_index().groupby('position_group')['price'].first(),
            'exit_date' : price_data.reset_index().groupby('position_group_day_after').date.last(),
            'exit_price' : price_data.reset_index().groupby('position_group_day_after')['price'].last(),
            'position_length' : price_data.groupby('position_group').size(),
            'position' : price_data.groupby('position_group').position.first()
        }).reset_index(drop=True)

    # Remove trades with neutral position
    trades = trades[trades.position != 0].reset_index(drop=True)

    trades['profitable'] = np.where(
        trades['position'] == 1, trades['exit_price'] > trades['enter_price'],
        trades['exit_price'] < trades['enter_price']
    )

    trades['pips'] = np.where(
        trades['position'] == 1,
        (trades['exit_price'] - trades['enter_price']) / 0.0001,
        (trades['enter_price'] - trades['exit_price']) / 0.0001
    )

    if stop_pips:
        # Calculate stop price from stop_pips
        trades['stop_price'] = np.where(
            trades['position'] == 1,
            trades['enter_price'] - (0.0001 * stop_pips),
            trades['enter_price'] + (0.0001 * stop_pips)
        )

        # Was the stop triggered or not
        trades['stop_triggered'] = np.where(
            trades['position'] == 1,
            trades['exit_price'] < trades['stop_price'],
            trades['exit_price'] > trades['stop_price']
        )

        # Recaulculate exit price if the stop was triggered
        trades['exit_price'] = np.where(
            trades['stop_triggered'] == True,
            trades['stop_price'],
            trades['exit_price']
        )

        # Recaulculate pips if the stop was triggered
        trades['pips'] = np.where(
            (trades['stop_triggered'] == True) & (trades['position'] == 1),
            (trades['exit_price'] - trades['enter_price']) / 0.0001,
            trades['pips']
        )
        trades['pips'] = np.where(
            (trades['stop_triggered'] == True) & (trades['position'] == -1),
            (trades['enter_price'] - trades['exit_price']) / 0.0001,
            trades['pips']
        )

    return trades
