# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_positions(positions, columns_to_keep = []):
    '''
    Creates a plot of the price with coloured bands to show the position
    '''
    # Create position groups
    positions['position_group'] = (positions['position'].diff(1) != 0).astype('int').cumsum()
    positions['position_group_day_after'] = positions['position_group'].shift(1)

    positions_to_plot = positions.copy()

    for column in positions_to_plot.columns:
        if column != 'price' and column not in columns_to_keep:
            positions_to_plot.drop(column, 1, inplace=True)

    ax = positions_to_plot.plot()
    ymax = positions_to_plot['price'].max()
    ymin = positions_to_plot['price'].min()

    non_zero_positions = positions[positions.position != 0]
    position_groups = list(set(non_zero_positions['position_group'].tolist()))

    print('{0} positions to plot...'.format(len(position_groups)))

    for group in position_groups:
        enter_loc = non_zero_positions.loc[non_zero_positions['position_group'] == group].index[0]
        exit_loc = non_zero_positions.loc[non_zero_positions['position_group'] == group].index[-1]
        position = non_zero_positions.loc[non_zero_positions['position_group'] == group]['position'][0]

        if position == 1:
            color = '#72a8ff'
        else:
            color = '#ff9e9e'

        ax.fill_between([enter_loc, exit_loc], ymin, ymax, color=color)
        ax.annotate('LONG', (0,0), (0, -60), xycoords='axes fraction', textcoords='offset points', va='top', size="large", color='#72a8ff')
        ax.annotate('SHORT', (0,0), (80, -60), xycoords='axes fraction', textcoords='offset points', va='top', size="large", color='#ff9e9e')

    plt.title('Positions', size='x-large')

    return ax
