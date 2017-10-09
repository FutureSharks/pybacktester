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
stats, results, trades = pybacktester.run_backtest(
  positions.copy(),
  portfolio_value=10000,
  position_percentage=2,
  stop_pips=3,
  spread_pips=1.3
)

# Show some stats for the backtest
print(stats)
{
  'win_loss_ratio': 0.46875,
  'start_portfolio_value': 10000.0,
  'end_portfolio_value': 56045576.016318738,
  'portfolio_lowest_value': 10000.0,
  'trades': 47,
  'total_pips': 829.43774693721605,
  'pips_per_win_trade': 61.527153115233268,
  'pips_per_loss_trade': -2.9209234309775929,
  'drawdown_percent_max': 33.048933752098037,
  'drawdown_percent_median': 11.639999999998757,
  'drawdown_percent_95th': 29.507298956442686,
  'win_percent_median': 90.35745762713265,
  'win_length_median': 20.0,
  'loss_length_median': 4.0,
  'return_percent': 560455.7601631874,
  'profit_factor': 8.4076426982340262
}

# Plot of trades showing trade outcome in colour
graph = pybacktester.plot_trades(positions.copy(), trades.copy())
plt.show()
```

![back-test-img2](../master/img/trade_plot.png?raw=true)


#### Run Monte Carlo simulation

```python
monte_carlo_results = pybacktester.run_monte_carlo(
    trades.copy(),
    runs=1000,
    portfolio_value=10000,
    position_percentage=2
)

print(monte_carlo_results)

{
  'mc_median_drawdown_percent_median': 11.639999999998762,
  'mc_median_drawdown_percent_max': 37.06599772697169,
  'mc_median_drawdown_percent_95th': 32.24627226242184,
  'mc_median_profit_factor': 4.448013213555316
}
```
