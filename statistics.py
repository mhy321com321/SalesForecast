import extract
import pandas as pd
from pandas import DataFrame as df
from datetime import datetime, timedelta

items = extract.items
prices = extract.prices
sales = extract.sales
ItemKeyName = ['pid', 'size']

# focus on items with static prices
# treat prices as a feature
# ~ # ----------------------------------------------------------

statCondition = prices.std() < 0.00001

statPrices = prices.mean()[statCondition]    # Series as outcome
statPrices.name = 'rtp'

ttlSales = sales.groupby(ItemKeyName)['cumUnits'].max()    # secure using .max(); efficienter using .last()

statSales = ttlSales[statCondition]
statSales.name = 'ttlSales'

statItems = items[statCondition]
statItems = pd.concat([statItems, statPrices], axis=1)
statItems = pd.concat([statItems, statSales], axis=1)
statItems['rate(0.01Unit)'] = statItems['ttlSales']*100/(datetime(2018, 1, 31) - statItems['releaseDate']).dt.days


