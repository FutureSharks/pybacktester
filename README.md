# pybacktester

![back-test-img1](../master/img/back_tester.jpg?raw=true)

A simple python3 vector based trade backtesting tool.

## Example

```python
import matplotlib.pyplot as plt
import pandas as pd
import pybacktester
import fx_data
from strategies import ma_bandwidth as strategy

# Get price data
price_data = fx_data.get(provider='sentdex', year='2013', month='05', day='01')
# Generate positions from the strategy
positions = strategy.apply(price_data.copy(), moving_average=25, bandwidth_pips=8)
# Show some stats for the backtest
stats, results, trades = pybacktester.run_backtest(positions.copy(), 10000, 7, stop_pips=3, spread_pips=1.3)

print(stats)
{
  'position_percentage': 7,
  'win_loss_ratio': 0.5,
  'end_portfolio_value': 21644.0,
  'start_portfolio_value': 10000,
  'portfolio_lowest_value': 14481.0,
  'trades': 4,
  'total_pips': 17.60000000000206,
  'pips_per_trade': 4.400000000000515,
  'median_position_length': 11.0,
  'return_percent': 116.44
}

# Show a graph on price and positions in colour
graph = pybacktester.plot_trades(positions.copy(), trades.copy())
plt.show(block=False)
# See below for graph
```

![back-test-img2](../master/img/graph_example.png?raw=true)
