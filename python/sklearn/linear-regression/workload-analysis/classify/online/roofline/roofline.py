#!/usr/bin/env python3

from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns;

def get_data(data_file_path):
    data_file_reader = open(data_file_path, 'r')
    data_list = []
    try:
        text_lines = data_file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            source, layer_name,	layer_type, exe_time, IN, IC, IH, IW, kernel_size, stride, pad,	ON, OC,	OH, OW,	flot_ops, mem_bytes, gflops, mem_band, op_intensity = line.split('\t')
            print(layer_type, float(gflops), float(op_intensity))
            data_list.append((layer_type, float(gflops), float(op_intensity)))
    finally:
        data_file_reader.close()
    return data_list

def draw_roofline(data_list, peak_flops, peak_membdw):
    layer_type_set = {record[0] for record in data_list}
    #print(layer_type_set)
    colors = sns.color_palette("hls", n_colors=len(layer_type_set) + 2)
    layer_color_map = {val:i for i, val in enumerate(list(layer_type_set))}
    #print(layer_color_map)
    fig, ax = plt.subplots(figsize=(6, 6))

    # 1. plot the <flops, intensity> pairs
    for i in data_list:
        layer_type, flops, intensity = str(i[0]), i[1], i[2]
        if layer_type == 'Convolution':
            ax.plot(intensity, flops, 'x',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='x')
        elif layer_type == 'InnerProduct':
            ax.plot(intensity, flops, 'v',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='v')
        elif layer_type == 'Pooling':
            ax.plot(intensity, flops, '*',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='*')
        elif layer_type == 'Scale':
            ax.plot(intensity, flops, 's',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='s')
        elif layer_type == 'Eltwise':
            ax.plot(intensity, flops, 'd',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='d')
        elif layer_type == 'ReLU':
            ax.plot(intensity, flops, 'p',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='p')
        elif layer_type == 'BatchNorm':
            ax.plot(intensity, flops, 'o',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='o')
        elif layer_type == 'LRN':
            ax.plot(intensity, flops, '^',
                    color=colors[layer_color_map[layer_type]], label=layer_type, marker='^')

    # 2. plot the roof line
    x1 = peak_flops / peak_membdw
    y1 = peak_flops
    max_op_intensity = max([i[2] for i in data_list])
    ax.hlines(y=y1, xmin=x1,
        xmax=max_op_intensity, linewidth=1.5, color='red')
    min_flops = min([i[1] for i in data_list])
    x2 = min_flops / peak_membdw
    y2 = peak_membdw * x2
    ax.plot([x1, x2], [y1, y2], linewidth=1.5, color='red')

    ax.set_yscale('log')
    ax.set_xscale('log')
    #plt.xscale('log', basex=2)
    #plt.yscale('log', basey=2)
    ax.set_ylabel('GFLOPS', fontsize=10)
    ax.set_xlabel('Operational Intensity (FLOPS/Byte)', fontsize=10)

    handles, labels = ax.get_legend_handles_labels()
    #print(labels)
    labels_od = OrderedDict(zip(labels, handles))
    ax.legend(labels_od.values(), labels_od.keys(), loc='upper left')

    plt.show()

if __name__ == '__main__':
    data = get_data('data.txt')
    # FLOPS: fp16 dense 0.5T, fp16 sparse 2T; int8 dense 1T, int8 sparse 4T
    #peak_flops = 16384
    peak_flops = 512
    # memory bandwidth: 25.6 GB/s, in real only reach 80%
    #peak_mem_bandwidth = 102.4
    peak_mem_bandwidth = 25.6
    draw_roofline(data, peak_flops, peak_mem_bandwidth)
