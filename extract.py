import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, ion, show    # interactive ploting
from pandas import DataFrame as df

Source = "~/Documents/repositories/SalesForecast/Source"
ItemKeyName = ['pid', 'size']

items = df.from_csv(path=Source+"/items.csv", sep='|')
prices = df.from_csv(path=Source+"/prices.csv", sep='|')
sales = df.from_csv(path=Source+"/train.csv", sep='|')


# reshape DataFrame
# ~ # ----------------------------------------------------------

# column(s) to index
items.set_index(['size'], append=True, inplace=True)
prices.set_index(['size'], append=True, inplace=True)
prices = prices.transpose()

# convert data type for index
prices = prices.reindex(pd.to_datetime(prices.index))

# cumulatively sold units for each item
# data['sum_Times']=data['Times'].groupby(['userID']).cumsum()    # know about it
sales = sales.sort_values(by=['pid', 'size'])
sales.loc[:, 'cumUnits'] = sales.groupby(ItemKeyName)['units'].cumsum()
sales.set_index(keys=ItemKeyName, append=True, inplace=True)
sales = sales.swaplevel(i='date', j='pid')
sales = sales.swaplevel(i='date', j='size')

""" reshaped items, prices and sales
In [1]: items
                 color   brand       rrp ...
pid    size
10001  L       schwarz    Jako     38.03 ...
10006  XL         blau  Armour     57.08 ...
...

In [2]: prices
       pid     19671              ...
      size    39 1/3        40    ...
date
2017-10-01    133.31    133.31    ...
2017-10-02    133.31    133.31    ...
...

In [3]: sales
                           units  cumUnits
pid    size    date
10000  XL      2017-11-20      1         1
10001  L       2017-11-25      1         1
...
"""


# visualization
# ~ # ----------------------------------------------------------

def plt_prices(dfPrices):
    """ print curves of goods prices

    Parameters
    ----------
    dfPrices : DataFrame or Series to be illustrated

    Returns
    -------
    None
    """
    plt.show(dfPrices.plot())

def plt_curves_by_item(subItem, factor=10):
    """https://blog.csdn.net/autoliuweijie/article/details/51594373
    """
    dfCurves = get_curves_by_item(subItem)

    dfCurves.loc[:, 'units'] = dfCurves.loc[:, 'units']*factor # adjust scale of sales
    dfCurves.loc[:, 'units'] = dfCurves.loc[:, 'units'].fillna(0)
    dfCurves.loc[:, 'cumUnits'] = dfCurves.loc[:, 'units'].cumsum()
    dfCurves.plot()
    

# inquire, merge, join etc.
# ~ # ----------------------------------------------------------

def get_items_by_prices(subPrices):
    """get information of items showing certain characters in DataFrame Prices.

    Parameters
    ----------
    subPrices : DataFrame filtered from Prices

    Returns
    -------
    subItems : DataFrame
    """
    itemKeys = subPrices.columns.values
    return items.loc[itemKeys ,:]

def get_curves_by_item(subItem):
    """get curves of prices and sales by item with certain characters in DataFrame items
    
    Parameters
    ----------
    subItem : tuple in form of (pid, 'size')
    """
    prc = prices.xs(key=subItem, axis=1)
    prc.name = 'prices'
    sal = sales.xs(key=subItem, level=ItemKeyName)
    return pd.concat([prc, sal], axis=1)
