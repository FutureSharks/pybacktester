# Forex Data

Oanda example:

```python
import fx_data
price_data = fx_data.get(provider='oanda', instrument='GBP_USD', year=2011, month=1)
```

Sentdex example:

```python
import fx_data
price_data = fx_data.get(provider='sentdex', year='2013', month='05', day='01')
```

Truefx example:

```python
import fx_data
price_data = fx_data.get(provider='truefx', year='2015', month='01', day='01')
```
