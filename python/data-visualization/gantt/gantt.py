# coding=utf-8
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
add=[[14,6,23],[18,7,35],[10,30,21],[18,5,30],[10,25,20],[12,35,20],[10,32,17],[10,20,16]]
left=[[0,14,20],[14,32,43],[32,42,78],[42,72,99],[60,77,129],[70,102,149],[82,137,169],[92,169,189]]
m = range(len(add))
n=range(len(add[0]))
color = ['b','g','r','y','c','m','k']

plt.figure(figsize=(20,8),dpi=80)
for i in m:
    for j in n:
        plt.barh(m[i]+int(i/5), add[i][j], left=left[i][j],color=color[j])
plt.title('Pipeline gantt chart')
labels =[''] *len(add[0])
for f in n:
    labels[f] = "P%d"%(f+1)

patches = [ mpatches.Patch(color=color[i], label="{:s}".format(labels[i]) ) for i in range(len(add[0])) ]
plt.legend(handles=patches,loc=4)
plt.xlabel('pieces/s')
plt.ylabel('Priority')
#plt.grid(linestyle="--",alpha=0.5)
plt.show()
