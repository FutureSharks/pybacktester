# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_equity(trades):
    '''
    Creates a plot of equity from trades
    '''
    
    return trades.set_index('exit_date').plot(y=['portfolio_value_after'])
