#!/usr/bin/env python
# Jiangsu College Entrance Examination, Problem 14

import numpy as np
import math
import matplotlib.pyplot as plt
from mpl_toolkits.axisartist.axislines import SubplotZero

# f(x) is a circle
def _f(x):
    if x >= 0 and x <= 2:
        return float(math.sqrt(1 - (x - 1)**2))
    if x > 2 and x <= 4:
        return float(-math.sqrt(1 - (x - 3)**2))
    if x > 4 and x <= 6:
        return float(math.sqrt(1 - (x - 5)**2))
    if x > 6 and x <= 8:
        return float(-math.sqrt(1 - (x - 7)**2))
    if x > 8 and x <= 9:
        return float(math.sqrt(1 - (x - 9)**2))


# g(x) is line segment
def _g(x, k = float(1/3.0)):
    if x == 0:
        return -0.5
    if x > 0 and x <= 1:
        return float(k * (x + 2))
    if x > 1 and x <= 2:
        return float(-0.5)
    if x > 2 and x <= 3:
        return _g(x - 2, k)
    if x > 3 and x <= 4:
        return float(-0.5)
    if x > 4 and x <= 5:
        return _g(x - 4, k)
    if x > 5 and x <= 6:
        return float(-0.5)
    if x > 6 and x <= 7:
        return _g(x - 6, k)
    if x > 7 and x <= 8:
        return float(-0.5)
    if x > 8 and x <= 9:
        return _g(x - 8, k)

if __name__ == '__main__':
    fig = plt.figure(1, (10, 6))
    ax = SubplotZero(fig, 1, 1, 1)
    fig.add_subplot(ax)
    ax.axis["xzero"].set_visible(True)
    ax.axis["xzero"].label.set_color('green')
    ax.axis["xzero"].set_axisline_style("-|>")
    ax.grid(True, linestyle='-.')
    #plt.figure(figsize=(6,4))
    x = np.linspace(0, 9, 1000)
    f_x = np.array([])
    g_x = np.array([])
    g_x_ = np.array([])

    # f(x)
    for dx in x:
    	f_x = np.append(f_x, np.linspace(_f(dx), _f(dx), 1))
    	g_x = np.append(g_x, np.linspace(_g(dx), _g(dx), 1))
    	g_x_ = np.append(g_x_, np.linspace(_g(dx, float(math.sqrt(2) / 4.0)), _g(dx, float(math.sqrt(2) / 4.0)), 1))

    plt.plot(x, f_x, 'b', label='f(x)')
    plt.plot(x, g_x, 'r', label='g(x), k = 1/3')
    plt.plot(x, g_x_, 'g', label='g(x), k = sqrt(2)/4')
    plt.legend()
    plt.show()
