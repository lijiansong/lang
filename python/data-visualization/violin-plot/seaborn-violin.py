import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# create test data
np.random.seed(19680801)
data = [sorted(np.random.normal(0, std, 100)) for std in range(1, 5)]

ax = sns.violinplot(x=data)
ax.set_xlabel('Observed values')

plt.show()
