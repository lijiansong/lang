import matplotlib.ticker as ticker
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.gridspec import GridSpec

import matplotlib.pyplot as plt
#%matplotlib inline
#credit https://matplotlib.org/devdocs/gallery/pie_and_polar_charts/pie_demo2.html#sphx-glr-gallery-pie-and-polar-charts-pie-demo2-py

source_labels = pie_sources.FoodCode.sort_values().index
source_counts = pie_sources.FoodCode.sort_values()

flavor_labels = pie_flavors.Source.sort_values().index
flavor_counts = pie_flavors.Source.sort_values()

# Make square figures and axes
plt.figure(1, figsize=(20,10))
the_grid = GridSpec(2, 2)

cmap = plt.get_cmap('Spectral')
colors = [cmap(i) for i in np.linspace(0, 1, 8)]

plt.subplot(the_grid[0, 1], aspect=1, title='Source of Pies')
source_pie = plt.pie(source_counts, labels=source_labels, autopct='%1.1f%%', shadow=True, colors=colors)
plt.subplot(the_grid[0, 0], aspect=1, title='Selected Flavors of Pies')

flavor_pie = plt.pie(flavor_counts,labels=flavor_labels, autopct='%.0f%%', shadow=True, colors=colors)
plt.suptitle('Pie Consumption Patterns in the United States', fontsize=16)
plt.show()
