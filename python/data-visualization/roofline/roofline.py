import os
import json
import matplotlib
import matplotlib.pyplot as plt

import numpy as np
import seaborn as sns;

colors = sns.color_palette("hls", n_colors=11)

'''
Get the range of hyperparameters from a list of labels.
'''
def get_range(labels, p=True):
    keywords = []
    for i in labels[0].split('-'):
        keywords.append(i.split('_')[0])

    values = []
    for i in range(len(keywords)):
        values.append(set())

    for f in labels:
        f_split = f.split('.')[0].split('-')
        for i in range(len(f_split)):
            values[i].add(int(f_split[i].split('_')[1]))
    results = {}
    for i in range(len(keywords)):
      if p == True:
        print(keywords[i], sorted(list(values[i])))
      results[keywords[i]] = sorted(list(values[i]))
    if p == True:
      print('-----------------------')
    return results

'''
Read a json file, return a dict.
'''
def get_data(filename = ''):
    if not os.path.isfile('./data/' + filename + '.json'):
      print('./data/' + filename + '.json', 'does not exist.')
      return None
    with open('./data/' + filename + '.json', 'r') as infile:
        d = json.load(infile)
    if 'tpu' in filename and 'flops' in d:
        # Note that in this case we will NOT reach here.
        d['flops'] = np.multiply(d['flops'] ,8)
    #print(d)
    return d

'''
Filter a dict of data based on range of hyperparameters specified by 'rule'.
'''
def filter_data(rule, data):
    keys = []
    new_data = {}
    for k,v in data.items():
        if k == 'err_jobs' or k == 'states':
            continue
        new_data[k] = []
        keys.append(k)
    for i in range(len(data['labels'])):
        f = 0
        l = data['labels'][i]
        for j in l.split('-'):
            if j.split('_')[0] in rule and \
                not int(j.split('_')[1]) in rule[ j.split('_')[0]]:
                f = 1
                break
        if f == 0:
            for k in keys:
                new_data[k].append(data[k][i])
    return new_data

def get_n_from_label(l, dim):
    if dim == 'op':
        return l.split('_')[-1].strip('0123456789-')
    for i in l.split('-'):
        if dim in i:
            return i.split('_')[-1]
    return None


def plot_roofline(f, ax, d, tpu_peak, membdw_peak, \
                  scale='absolute', color_map={}, color_dim='', color=0, thre=1, label='', title=''):

    colormap = {}
    if scale == 'absolute':
      flops = np.multiply(d['flops_perc'], tpu_peak/100)
    else:
      flops = d['flops_perc']

    labels = d['labels']
    intensity = d['intensity']
    time = d['time_perc']
    if color_dim == '':
        if color == 0:
          ax.plot(d['intensity'], flops, '.', label=label)
        else:
          ax.plot(d['intensity'], flops, '.', label=label, color=color, alpha=0.9)
    else:
        hist = {}
        for i in range(len(labels)):
            l = d['labels'][i]
            n = get_n_from_label(l, color_dim)
            if time[i] < thre:
              continue
            if intensity[i]<=0 or flops[i]<=0:
              continue
            if not n in hist:
                hist[n] = 0
            hist[n] += 1
        for k,v in hist.items():
            hist[k] = v*1.0/len(labels)

        m = {}
        mycolors = sns.color_palette("hls", n_colors=len(hist)+2)
        for i in range(len(labels)):
            if time[i] < thre:
              continue
            if intensity[i]<=0 or flops[i]<=0:
              continue
            l = labels[i]
            n = get_n_from_label(l, color_dim)

            if color_map != {}:
                if n in color_map:
                    if n in m:
                      ax.plot(intensity[i], flops[i], '.', color=color_map[n], marker='.')
                    else:
                      ax.plot(intensity[i], flops[i], '.', color=color_map[n], marker='.', label = n)
                      m[n] = 1
                continue
            if n in m:
                ax.plot(intensity[i], flops[i], '.',
                        color=mycolors[m[n]], marker='.')
            elif not n in m:

                m[n] = len(m) % len(colors)
                colormap[n] = mycolors[m[n]]
                ax.plot(intensity[i], flops[i], '.',
                        color=mycolors[m[n]], label = n,
                        #markeredgecolor='black', markeredgewidth=0.5,
                        marker='.')
        if color_dim != 'op':
            handles, ls = ax.get_legend_handles_labels()
            ls = [int(i) for i in ls]
            ls, handles = zip(*sorted(zip(ls, handles), key=lambda t: t[0]))
            ls = [color_dim + '-' + str(i) for i in ls]
            ax.legend(handles, ls, frameon=True)
        else:
            ax.legend(frameon=True, bbox_to_anchor=(1, 0.5))

    x1 = tpu_peak / membdw_peak
    y1 = tpu_peak

    if max(d['intensity']) > x1:
        if color == 0:
            ax.hlines(y=y1, xmin=x1,
                xmax=max(d['intensity']), linewidth=2, color=colors[0])
        else:
            ax.hlines(y=y1, xmin=x1,
                xmax=max(d['intensity']), linewidth=2, color=color)

    x2 = min(d['flops_perc'])*(tpu_peak/100)/membdw_peak
    y2 = min(d['flops_perc'])*(tpu_peak/100)

    if scale == 'relative':
        y1 = 100
        y2 = x2 * membdw_peak / tpu_peak * 100
    if color == 0:
        ax.plot([x1, x2], [y1, y2], linewidth=2, color=colors[0])
    else:
        ax.plot([x1, x2], [y1, y2], linewidth=2, color=color)

    ax.set_yscale('log')
    ax.set_xscale('log')
    if scale == 'absolute':
      ax.set_ylabel('GFLOPS', fontsize=15)
    else:
      ax.set_ylabel('FLOPS %', fontsize=15)
      ax.set_ylim(top=100)
    ax.set_xlabel('Floating Ops/Byte', fontsize=15)
    ax.set_title(title, fontsize=15)

    if colormap == {}:
        colormap = color_map
    return f, ax, colormap

if __name__ == '__main__':
    color_dim = 'node'
    d = get_data('fc_trace_10sec')
    #get_range(d['labels'])
    d = filter_data({'bs':[512, 1024, 2048, 4096, 8192, 16384], 'node':[128, 512, 2048, 8192]}, d)
    #print(d)
    f, ax = plt.subplots(figsize=(6, 6))
    f, ax, m = plot_roofline(f, ax, d, tpu_peak=180e3, membdw_peak=2400, color_dim=color_dim, title='')

    # sort the legend
    handles, ls = ax.get_legend_handles_labels()
    ls = [int(i) for i in ls if i.isdigit()]
    ls, handles = zip(*sorted(zip(ls, handles), key=lambda t: t[0]))
    ls = [color_dim + '-' + str(i) for i in ls]
    ax.legend(handles, ls, frameon=True, fontsize=10)
    plt.show()
