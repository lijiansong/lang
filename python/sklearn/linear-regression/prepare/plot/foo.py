import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
data = np.random.rand(10, 12)
f, ax = plt.subplots(figsize=(8,5))
ax = sns.heatmap(data,cmap = 'RdBu',ax=ax,vmin=0, vmax=1,annot=True,fmt ='0.1g')

#设置坐标字体方向
label_y = ax.get_yticklabels()
plt.setp(label_y, rotation=45, horizontalalignment='right')
label_x = ax.get_xticklabels()
plt.setp(label_x, rotation=45, horizontalalignment='right')
plt.xlabel('x.num')#设置坐标名称
plt.ylabel('y.num')
plt.title('Plotting')#标题
plt.show()
