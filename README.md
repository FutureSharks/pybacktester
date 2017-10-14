# pybacktester

![back-test-img1](../master/img/back_tester.jpg?raw=true)

A simple python3 vector based trade backtesting tool.

Here is an example Jupyter Notebook using a common triple moving average strategy:

[triple_ema_crossover.ipynb](jupyter-notebooks/triple_ema_crossover.ipynb)

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
  risk_percentage=1,
  stop_pips=3,
  spread_pips=1.3
)

# Show some stats for the backtest
print(stats)

{
  'win_loss_ratio': 0.10638297872340426,
  'trades': 47,
  'trades_per_day': 1.6206896551724137,
  'total_pips': 237.17369690168692,
  'pips_per_win_trade': 72.128649338593306,
  'pips_per_loss_trade': -2.9397511855066591,
  'win_length_median': 22.0,
  'loss_length_median': 6.0,
  'pip_profit_factor': 2.9209084126622269,
  'start_portfolio_value': 10000.0,
  'end_portfolio_value': 18697.792374075601,
  'return_percent': 86.977923740756012,
  'portfolio_lowest_value': 10000.0,
  'win_percent_median': 19.417178063509873,
  'drawdown_percent_max': 17.932256889942789,
  'drawdown_percent_median': 7.725530557207986,
  'drawdown_percent_95th': 16.165324893562378,
  'profit_factor': 2.4857426605107258
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
    risk_percentage=1
)

print(monte_carlo_results)

{
  'mc_median_drawdown_percent_median': 5.879891747194882,
  'mc_median_drawdown_percent_max': 15.273020036511578,
  'mc_median_drawdown_percent_95th': 14.214037605327032,
  'mc_median_profit_factor': 2.486943907983055
}
```
