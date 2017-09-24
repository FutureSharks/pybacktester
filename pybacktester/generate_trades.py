# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def generate_trades(price_data, spread_pips, stop_pips, slippage_pips):
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
            'enter_date': price_data.reset_index().groupby('position_group').date.first(),
            'enter_price': price_data.reset_index().groupby('position_group')['price'].first() + (
                price_data.groupby('position_group').position.first() * (
                    # Add spread
                    (0.0001 * (spread_pips / 2)) +
                    # Add splippage
                    (0.0001 * slippage_pips)
                )
            ),
            'in_trade_price_min': price_data.reset_index().groupby('position_group')['price'].min(),
            'in_trade_price_max': price_data.reset_index().groupby('position_group')['price'].max(),
            'exit_date': price_data.reset_index().groupby('position_group_day_after').date.last(),
            'exit_price': price_data.reset_index().groupby('position_group_day_after')['price'].last() - (
                price_data.groupby('position_group').position.first() * (
                    # Add spread
                    (0.0001 * (spread_pips / 2)) +
                    # Add splippage
                    (0.0001 * slippage_pips)
                )
            ),
            'position_length': price_data.groupby('position_group').size(),
            'position': price_data.groupby('position_group').position.first()
        }).reset_index(drop=True)

    # Remove trades with neutral position
    trades = trades[trades.position != 0].reset_index(drop=True)

    # Calculate stop price from stop_pips
    trades['stop_price'] = np.where(
        trades['position'] == 1,
        trades['enter_price'] - (0.0001 * stop_pips),
        trades['enter_price'] + (0.0001 * stop_pips)
    )

    # Was the stop triggered or not
    trades['stop_triggered'] = np.where(
        trades['position'] == 1,
        (trades['in_trade_price_min'] < trades['stop_price']) | (trades['exit_price'] < trades['stop_price']),
        (trades['in_trade_price_max'] > trades['stop_price']) | (trades['exit_price'] > trades['stop_price'])
    )

    # Recaulculate exit price if the stop was triggered
    trades['exit_price'] = np.where(
        trades['stop_triggered'] == True,
        trades['stop_price'],
        trades['exit_price']
    )

    # Was each trade profitable
    trades['profitable'] = np.where(
        trades['position'] == 1,
        trades['exit_price'] > trades['enter_price'],
        trades['exit_price'] < trades['enter_price']
    )

    # Calculate number of pips won or lost
    trades['pips'] = np.where(
        trades['position'] == 1,
        (trades['exit_price'] - trades['enter_price']) / 0.0001,
        (trades['enter_price'] - trades['exit_price']) / 0.0001
    )

    # Drop in_trade_price_max and in_trade_price_min as these are not required
    trades.drop('in_trade_price_max', 1, inplace=True)
    trades.drop('in_trade_price_min', 1, inplace=True)

    return trades
