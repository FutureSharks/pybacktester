# Oanda Price Data

History FX prices can be downloaded from Oanda if you have an account with them, even a free practice account is enough.


```python
from pybacktester import get_oanda_prices

instrument = 'EUR_USD'

for year in range(2005, 2018):
    for month in range(1, 13):
        get_oanda_prices(
            csv_file='fx_data/data/oanda/{0}/{1}/oanda-{0}-{1}-{2}.csv'.format(
                instrument,
                year,
                month
            ),
            instrument=instrument,
            year=year,
            month=month
        )

```
