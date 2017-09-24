# pybacktester

![back-test-img1](../master/img/back_tester.jpg?raw=true)

A simple python3 vector based trade backtesting tool.

Here is an example Jupyter Notebook using a common triple moving average strategy:

[triple_ema_crossover.ipynb](triple_ema_crossover.ipynb)

### Example

#### Generating positions

```python
import matplotlib.pyplot as plt
import pandas as pd
import pybacktester
import fx_data

# Import a strategy to backtest
from strategies import triple_ema_crossover as strategy

# Get price data
price_data = fx_data.get(provider='oanda', instrument='GBP_USD', year=2011, month=1, time_group='60min')
# Generate positions from the strategy
positions = strategy.apply(price_data.copy(), slow_ema=18, medium_ema=9, fast_ema=4)
# Show positions on a graph
position_graph = pybacktester.plot_positions(positions.copy())
plt.show()
```

![back-test-img2](../master/img/position_plot.png?raw=true)


#### Run a backtest

```python
stats, results, trades = pybacktester.run_backtest(positions.copy(), 10000, 2, stop_pips=3, spread_pips=1.3)

# Show some stats for the backtest
print(stats)
{
  'end_portfolio_value': 56045576.0,
  'median_position_length': 8.0,
  'pips_per_trade': 17.647611636962043,
  'portfolio_lowest_value': 31142.0,
  'position_percentage': 2,
  'return_percent': 560355.76000000001,
  'start_portfolio_value': 10000,
  'total_pips': 829.43774693721605,
  'trades': 47,
  'win_loss_ratio': 0.31914893617021278
}

# Plot of trades showing trade outcome in colour
graph = pybacktester.plot_trades(positions.copy(), trades.copy())
plt.show()
```

![back-test-img2](../master/img/trade_plot.png?raw=true)
