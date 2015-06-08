import numpy as np
import pandas as pd
from matplotlib import pyplot

turnstile_weather = pd.read_csv('turnstile_master.csv')

l1 = pd.DataFrame(turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 1]).sort(['ENTRIESn_hourly'])[:40000]
l2 = pd.DataFrame(turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 0]).sort(['ENTRIESn_hourly'])[:80000]
    
l1 = l1['ENTRIESn_hourly'].tolist()
l2 = l2['ENTRIESn_hourly'].tolist()

print len(l1) - len(l2)

pyplot.hold(True)

pyplot.hist(l1, 50, alpha = 0.5, label = 'Rain')
pyplot.hist(l2, 50, alpha = 0.5, label = 'No rain')

pyplot.legend(loc='upper right')
pyplot.show()