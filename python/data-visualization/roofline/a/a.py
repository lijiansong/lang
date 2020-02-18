import os
import json
import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns;
import pickle

colors = sns.color_palette("hls", n_colors=11)

if __name__ == '__main__':
    flops_info_reader = open('flops_info.txt', 'rb')
    intensity_info_reader = open('intensity_info.txt', 'rb')
    flops = pickle.load(flops_info_reader)
    intensity = pickle.load(intensity_info_reader)
    print(flops)
    print(intensity)

    f, ax = plt.subplots(figsize=(6, 6))

    len_hist = 4
    mycolors = sns.color_palette("hls", n_colors=len_hist + 2)
    for i in range(len(flops)):
        l = ''
        if i%4 == 0:
            l = str(0)
        elif i%4 == 1:
            l = str(1)
        elif i%4 == 2:
            l = str(2)
        elif i%4 == 3:
            l = str(3)
        ax.plot(intensity[i], flops[i], '.',
                color=mycolors[i % 4], label=l, marker='.')

    handles, ls = ax.get_legend_handles_labels()
    _ls = {i for i in ls}

    #ls, handles = zip(*sorted(zip(ls, handles), key=lambda t: t[0]))
    ls = ['node-' + str(i) for i in _ls]
    ax.legend(handles, ls, frameon=True)
    #print(handles)
    print(ls)
    #ax.legend(handles, ls, frameon=True, fontsize=10)
    tpu_peak=180e3
    membdw_peak=2400
    # x1: 75.0
    x1 = tpu_peak / membdw_peak
    # y1: 180000.0
    y1 = tpu_peak
    max_d_intensity = 191.6364463810484
    ax.hlines(y=y1, xmin=x1,
        xmax=max_d_intensity, linewidth=2, color=colors[0])

    min_d_flops_perc = 0.25964698664028574
    # x2: 0.1947352399802143
    x2 = min_d_flops_perc*(tpu_peak/100)/membdw_peak
    # y2: 467.3645759525143
    y2 = min_d_flops_perc*(tpu_peak/100)
    # [x1, x2]: 75.0, 0.1947352399802143
    # [y1, y2]: 180000.0, 467.3645759525143
    ax.plot([x1, x2], [y1, y2], linewidth=2, color=colors[0])
    # Note in this mode (0, 0) will disappear
    #ax.plot([x1, 0], [y1, 0], linewidth=2, color=colors[0])
    ax.set_yscale('log')
    ax.set_xscale('log')
    ax.set_ylabel('GFLOPS', fontsize=15)
    ax.set_xlabel('Operational Intensity(Floating Ops/Byte)', fontsize=15)

    plt.show()
