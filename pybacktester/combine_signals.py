# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np


def combine_signals(trade_signals, trade_signals_confirmation):
    '''
    Takes a dataframe of trade signals and a second dataframe of signal confirmations.
    Returns a combined dataframe with positions.
    '''
    # Combine both
    combined_position = trade_signals.copy()
    combined_position['position_signal'] = trade_signals['position']
    combined_position['position_confirmation'] = trade_signals_confirmation['position']
    combined_position['position'] = np.where(combined_position['position_confirmation'] == 1, combined_position['position_signal'], 0)

    # Close last position
    combined_position.iloc[-1, combined_position.columns.get_loc('position')] = 0

    # Create position groups
    combined_position['position_group'] = (combined_position['position'].diff(1) != 0).astype('int').cumsum()
    combined_position['position_group_day_after'] = combined_position['position_group'].shift(1)

    return combined_position
