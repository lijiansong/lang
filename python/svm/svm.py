import numpy as np
from matplotlib import pyplot as plt

# REF: https://github.com/SSaishruthi/SVM-using-Numpy/blob/master/SVM.ipynb
#Input data
x = np.array([
    [-2,4,-1],
    [4,1,-1],
    [1, 6, -1],
    [2, 4, -1],
    [6, 2, -1],

])


#output label
y = np.array([-1, -1, 1, 1, 1])

for val, inp in enumerate(x):
    if y[val] == -1:
        plt.scatter(inp[0], inp[1], s=100, marker='_', linewidths=5)
    else:
        plt.scatter(inp[0], inp[1], s=100, marker='+', linewidths=5)

plt.plot([-2,6],[6,1])

def svm_function(x,y):
    #initilizing weight
    w = np.zeros(len(x[0]))
    #initialize learning rate
    l_rate = 1
    #epoch
    epoch = 100000
    #output list
    out = []
    #training svm
    for e in range(epoch):
        for i, val in enumerate(x):
            val1 = np.dot(x[i], w)
            if (y[i]*val1 < 1):
                w = w + l_rate * ((y[i]*x[i]) - (2*(1/epoch)*w))
            else:
                w = w + l_rate * (-2*(1/epoch)*w)
    
    for i, val in enumerate(x):
        out.append(np.dot(x[i], w))
    
    return w, out

w, out = svm_function(x,y)

print('Calculated weights')
print(w)

u = np.array([
    [-1,3,-1],
    [5,5,-1],
    
])
   
    
for val, inp in enumerate(x):
    if y[val] == -1:
        plt.scatter(inp[0], inp[1], s=100, marker='_', linewidths=5)
    else:
        plt.scatter(inp[0], inp[1], s=100, marker='+', linewidths=5)

plt.scatter(-1,3, s=100, marker='_', linewidths=5)   
plt.scatter(5,5, s=100, marker='+', linewidths=5)   


x1=[w[0],w[1],-w[1],w[0]]
x2=[w[0],w[1],w[1],-w[0]]

x1x2 =np.array([x1,x2])
X,Y,U,V = zip(*x1x2)
ax = plt.gca()
ax.quiver(X,Y,U,V,scale=1, color='blue')

u = np.array([
    [-1,3,-1],
    [5,5,-1],
    
])

result = []
for i, val in enumerate(u):
        result.append(np.dot(u[i], w))
print('test result')
print(result)
print('predicted output')
print(out)
