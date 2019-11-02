#!/usr/bin/env python3

import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import codecs

def plot_heatmap(file_name, xlabel_name, ylabel_name, xtick_labels, ytick_labels):
    file = open(file_name, "rb")
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
    _, ax = plt.subplots(figsize=(8, 5))
    #p1 = sns.heatmap(df, cmap='Reds', annot=True)
    #p1 = sns.heatmap(df, cmap='Reds')
    fig = sns.heatmap(df, cmap='Reds', ax=ax, cbar_kws={'label': 'End to end FPS'}, linewidths=0.01, linecolor='black')
    #fig = sns.heatmap(df, cmap='YlGnBu', cbar_kws={'label': 'End to end FPS'}, linewidths=.1)
    plt.xlabel(xlabel_name)
    plt.ylabel(ylabel_name)
    fig.set_xticklabels(xtick_labels)
    fig.set_yticklabels(ytick_labels)
    label_y = fig.get_yticklabels()
    plt.setp(label_y, rotation=45, horizontalalignment='right')
    label_x = fig.get_xticklabels()
    plt.setp(label_x, rotation=45, horizontalalignment='right')
    plt.show()

if __name__ == '__main__':
    bs_ticklabels = ['1', '2', '4', '8', '16', '32', '64', '128', '256', '512', '1024']
    tn_ticklabels = ['1', '2', '4', '8', '16', '32', '64', '128']
    mp_ticklabels = ['1', '2', '4', '8', '16', '32']
    dp_ticklabels = ['1', '2', '4', '8', '16', '32']
    plot_heatmap('bs_mp.txt', 'model parallelism', 'batch size', mp_ticklabels, bs_ticklabels)
    plot_heatmap('dp_mp.txt', 'model parallelism', 'data parallelism', mp_ticklabels, dp_ticklabels)
    plot_heatmap('bs_dp.txt', 'data parallelism', 'batch size', dp_ticklabels, bs_ticklabels)
    plot_heatmap('bs_tn.txt', 'thread number', 'batch size', tn_ticklabels, bs_ticklabels)

