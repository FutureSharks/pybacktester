# pybacktester

![back-test-img1](../master/img/back_tester.jpg?raw=true)

A simple python3 vector based trade backtesting tool.

## Example

```python
import matplotlib.pyplot as plt
import pandas as pd
import pybacktester
import fx_data
from strategies import strategy1 as strategy

# Get price data
price_data = fx_data.get(provider='sentdex', year='2013', month='05', day='01')
# Generate positions from the strategy
positions = strategy.apply(price_data.copy(), moving_average=3, ma_bandwidth_percent=0.010500)
# Generate trades from the position data
trades = pybacktester.generate_trades(positions.copy(), stop_pips=2)
# Show some stats for the backtest
stats, results = pybacktester.run_backtest(positions.copy(), 10000, 7, stop_pips=2)

print(stats)
{
  'position_percentage': 7,
  'win_loss_ratio': 0.61971830985915488,
  'end_portfolio_value': 82696.0,
  'start_portfolio_value': 10000,
  'portfolio_lowest_value': 9685.0,
  'trades': 71,
  'total_pips': 36.04999999999637,
  'pips_per_trade': 0.5077464788731884,
  'median_position_length': 1.0,
  'return_percent': 726.96000000000004
}

# Show a graph on price and positions in colour
graph = pybacktester.plot_trades(positions.copy(), trades.copy())
plt.show()
# See below for graph
```

![back-test-img2](../master/img/graph_example.png?raw=true)
