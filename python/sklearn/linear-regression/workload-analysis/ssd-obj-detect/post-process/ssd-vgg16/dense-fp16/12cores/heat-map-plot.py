#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import codecs

def plot_heatmap(in_file_name, out_fig_name, xlabel_name, ylabel_name, xtick_labels, ytick_labels):
    file = open(in_file_name, "rb")
    read_res = csv.reader(codecs.iterdecode(file, 'utf-8'), delimiter=',')
    data = list(read_res)
    print(type(data))
    for item in data:
        for i in range(len(item)):
            if item[i] == '':
                item[i] = np.nan
            else:
                item[i] = float(item[i])
    print(data)
    df = pd.DataFrame(data)
    print("data shape:", df.shape)
    _, ax = plt.subplots(figsize=(6, 5))
    #p1 = sns.heatmap(df, cmap='Reds', annot=True)
    #fig = sns.heatmap(df, cmap='Reds', ax=ax, cbar_kws={'label': 'End to end FPS'}, linewidths=0.01, linecolor='black')
    if 'hw' in in_file_name:
        fig = sns.heatmap(df, cmap='YlGnBu', ax=ax, cbar_kws={'label': 'Normalized hardware FPS'}, linewidths=0.01, linecolor='black')
    else:
        fig = sns.heatmap(df, cmap='YlGnBu', ax=ax, cbar_kws={'label': 'Normalized end-to-end FPS'}, linewidths=0.01, linecolor='black')
    #fig = sns.heatmap(df, cmap='YlGnBu', ax=ax, cbar_kws={'label': 'End to end FPS'}, linewidths=0.0, linecolor='black')
    plt.xlabel(xlabel_name)
    plt.ylabel(ylabel_name)
    fig.set_xticklabels(xtick_labels)
    fig.set_yticklabels(ytick_labels)
    label_y = fig.get_yticklabels()
    plt.setp(label_y, rotation=45, horizontalalignment='right')
    label_x = fig.get_xticklabels()
    plt.setp(label_x, rotation=45, horizontalalignment='right')
    #plt.savefig(out_fig_name)
    plt.show()

if __name__ == '__main__':
    bs_ticklabels = ['1', '2', '4', '8', '16', '32', '64']
    tn_ticklabels = ['1', '2', '4', '8', '16', '32', '64']
    mp_ticklabels = ['1', '2', '4', '8', '16', '32']
    dp_ticklabels = ['1', '2', '4', '8', '16', '32']
    plot_heatmap('bs_mp.txt', 'bs_mp.png', 'model parallelism', 'batch size', mp_ticklabels, bs_ticklabels)
    plot_heatmap('dp_mp.txt', 'dp_mp.png', 'model parallelism', 'data parallelism', mp_ticklabels, dp_ticklabels)
    plot_heatmap('bs_dp.txt', 'bs_dp.png', 'data parallelism', 'batch size', dp_ticklabels, bs_ticklabels)
    plot_heatmap('bs_tn.txt', 'bs_tn.png', 'thread number', 'batch size', tn_ticklabels, bs_ticklabels)
    plot_heatmap('tn_dp.txt', 'tn_dp.png', 'data parallelism', 'thread number', dp_ticklabels, tn_ticklabels)
    plot_heatmap('tn_mp.txt', 'tn_mp.png', 'model parallelism', 'thread number', mp_ticklabels, tn_ticklabels)
    plot_heatmap('hw-tn_dp.txt', 'hw-tn_dp.png', 'data parallelism', 'thread number', dp_ticklabels, tn_ticklabels)
    plot_heatmap('hw-tn_mp.txt', 'hw-tn_mp.png', 'model parallelism', 'thread number', mp_ticklabels, tn_ticklabels)
