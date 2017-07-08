# strategies

A strategy must return the a Pandas dataframe with the following columns:

1. `price` - The price of the thing
2. `position` - 1 for long, 0 for none, -1 for short
3. `date` - This is the index. Must be a pandas DatetimeIndex.
