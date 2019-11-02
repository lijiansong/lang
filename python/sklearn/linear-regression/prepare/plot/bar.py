import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
uniform_data = np.random.rand(10, 12)
f, ax = plt.subplots(figsize=(9, 6))
ax = sns.heatmap(uniform_data)
plt.show()
