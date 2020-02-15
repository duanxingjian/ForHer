import pandas as pd
import matplotlib as plt
import numpy as np
from matplotlib import pyplot

pd.set_option('display.expand_frame_repr', False)
plt.interactive(False)

# date,datatype,station,avg_temp,region
# 2018-04-27T00:00:00,TAVG,GHCND:USR0000JEBF,12.2,Northeast Climate Region
df = pd.read_csv("WeatherData.csv", header=0, parse_dates=['date']) \
    .set_index('date')

grouped = df.groupby([df.index.year, df.index.quarter, 'region'])
grouped = grouped["avg_temp"].median()
grouped.index = grouped.index.set_names(['year', 'quarter', 'region'])
grouped = grouped.reset_index()
#print(grouped)

group1 = grouped[(grouped["year"] == 2013) | (grouped["year"] == 2014) | (grouped["year"] == 2015)]
group1 = group1.groupby(['quarter', 'region'])["avg_temp"].median().unstack()

group2 = grouped[(grouped["year"] == 2016) | (grouped["year"] == 2017) | (grouped["year"] == 2018)]
group2 = group2.groupby(['quarter', 'region'])["avg_temp"].median().unstack()

print(group1)
print(group2)


grouped2 = grouped.groupby(['quarter', 'region'])
# grouped_plot1 = grouped2["avg_temp"].agg([np.var])
# grouped_plot2 = grouped2["avg_temp"].agg([np.std])

# print(grouped_plot1)
#
# grouped_plot1.unstack().plot()
# grouped_plot2.unstack().plot()
plt.pyplot.show()



# df_print = df_total.groupby(by=['region', pd.Grouper(freq='M')])["avg_temp"].mean()
# df1.plot(x='date', y='avg_temp')
# print(df_print)

regions = ['Northeast Climate Region',
           'East Northcentral Climate Region',
           'Central Climate Region',
           'Southeast Climate Region',
           'West Northcentral Climate Region',
           'South Climate Region',
           'Southwest Climate Region',
           'Northwest Climate Region',
           'West Climate Region']