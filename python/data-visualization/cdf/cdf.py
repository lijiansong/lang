from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

'''
REF: https://stackoverflow.com/questions/3209362/how-to-plot-empirical-cdf-in-matplotlib-in-python
'''
data=[14.27,14.80,12.28,17.09,15.10,12.92,15.56,15.38,
      15.15,13.98,14.90,15.91,14.52,15.63,13.83,13.66,
      13.98,14.47,14.65,14.73,15.18,14.49,14.56,15.03,
      15.40,14.68,13.33,14.41,14.19,15.21,14.75,14.41,
      14.04,13.68,15.31,14.32,13.64,14.77,14.30,14.62,
      14.10,15.47,13.73,13.65,15.02,14.01,14.92,15.47,
      13.75,14.87,15.28,14.43,13.96,14.57,15.49,15.13,
      14.23,14.44,14.57]
plt.subplot(121)
hist, bin_edges = np.histogram(data)
cdf = np.cumsum(hist)
plt.plot(bin_edges[1:], cdf)

plt.show()
