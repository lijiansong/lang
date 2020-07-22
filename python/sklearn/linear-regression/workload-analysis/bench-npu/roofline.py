#!/usr/bin/env python3

from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt

import seaborn as sns;

def extract_model_data(data_file_path, debug=True):
    data_file_reader = open(data_file_path, 'r')
    # key is net name, value is list of <batch size, gflops, intensity> tuples
    gflops_intensity_dict = {}
    try:
        text_lines = data_file_reader.readlines()
        # two lines, the first line is glops, the second is operational intensity
        for i, line in enumerate(text_lines):
            # extract the first line(GFLOPS) and then get the next line(Operational Intensity)
            if i % 2 == 0:
                # extract gflops
                current_line = line.rstrip('\n')
                gflops_list = current_line.split('\t')
                # extract operational intensity
                next_line = text_lines[i+1].rstrip('\n')
                intensity_list = next_line.split('\t')
                dict_values_list = []
                for j, item in enumerate(gflops_list):
                    # the first item is net name
                    if j == 0:
                        continue
                    # batch size, gflops, op intensity
                    dict_values_list.append((2**(j-1), float(item), float(intensity_list[j])))
                gflops_intensity_dict[gflops_list[0]] = dict_values_list
            else:
                continue
        if debug:
            print(gflops_intensity_dict)
    finally:
        data_file_reader.close()
    return gflops_intensity_dict

def extract_model_throughput(data_file_path, debug=True):
    data_file_reader = open(data_file_path, 'r')
    # key is net name, value is list of <batch size, gflops, intensity> tuples
    gflops_intensity_dict = {}
    try:
        text_lines = data_file_reader.readlines()
        for i, line in enumerate(text_lines):
            # extract gflops
            current_line = line.rstrip('\n')
            data_list = current_line.split('\t')
            net_name = data_list[0]
            # batch size is 1.
            dict_values_list = (1, float(data_list[1]), float(data_list[2]))
            if net_name not in gflops_intensity_dict:
                gflops_intensity_dict[net_name] = [dict_values_list]
            else:
                gflops_intensity_dict[net_name].append(dict_values_list)
        if debug:
            print(gflops_intensity_dict)
    finally:
        data_file_reader.close()
    return gflops_intensity_dict

def extract_op_data(data_file_path, debug=True):
    data_file_reader = open(data_file_path, 'r')
    # key is net name, value is list of <batch size, gflops, intensity> tuples
    op_data_list = []
    try:
        text_lines = data_file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            _, op_type, glops, intensity = line.split('\t')
            op_data_list.append((op_type, float(glops), float(intensity)))
        if debug:
            print(op_data_list)
    finally:
        data_file_reader.close()
    return op_data_list

# find out the max intensity and min gflops
def find_boundard_pairs(gflops_intensity_dict):
    max_intensity = -1
    min_flops = 1.79e+100
    for k, v in gflops_intensity_dict.items():
        for _, gflops, intensity in v:
            max_intensity = max(max_intensity, intensity)
            min_flops = min(min_flops, gflops)
    return max_intensity, min_flops

def draw_model_roofline(gflops_intensity_dict, peak_flops, peak_membdw):
    # set color palette for different dnns
    net_type_set = {k for k in gflops_intensity_dict}
    colors = sns.color_palette("hls", n_colors=len(net_type_set) + 2)
    net_color_map = {val:i for i, val in enumerate(list(net_type_set))}
    fig, ax = plt.subplots(figsize=(6, 6))

    # 1. plot the <flops, intensity> pairs
    for k, v in gflops_intensity_dict.items():
        # k is net name
        if k == 'MobileNetV1':
            for batch_size, gflops, intensity in v:
                ax.plot(intensity, gflops, 'x',
                        color=colors[net_color_map[k]], label=k, marker='x')
        elif k == 'SqueezeNet':
            for batch_size, gflops, intensity in v:
                ax.plot(intensity, gflops, 'v',
                        color=colors[net_color_map[k]], label=k, marker='v')
        elif k == 'DenseNet121':
            for batch_size, gflops, intensity in v:
                ax.plot(intensity, gflops, '*',
                        color=colors[net_color_map[k]], label=k, marker='*')
        elif k == 'ResNet50':
            for batch_size, gflops, intensity in v:
                ax.plot(intensity, gflops, 's',
                        color=colors[net_color_map[k]], label=k, marker='s')
        elif k == 'SSD_MobileNetV1':
            for batch_size, gflops, intensity in v:
                ax.plot(intensity, gflops, 'd',
                        color=colors[net_color_map[k]], label=k, marker='d')
        elif k == 'SSD_VGG16':
            for batch_size, gflops, intensity in v:
                ax.plot(intensity, gflops, 'p',
                        color=colors[net_color_map[k]], label=k, marker='p')

    # 2. plot the roof line
    x1 = peak_flops / peak_membdw
    y1 = peak_flops
    max_op_intensity, min_flops = find_boundard_pairs(gflops_intensity_dict)
    print('max intensity:', max_op_intensity, 'min flops:', min_flops)
    if max_op_intensity < x1:
        '''
        for this case:   -----
                             /
                            /*
                           /*
                          /* x
                         / x
        '''
        ax.hlines(y=y1, xmin=x1,
                xmax=x1+5, linewidth=1.5, color='red')
    else:
        ax.hlines(y=y1, xmin=x1,
                xmax=max_op_intensity+10, linewidth=1.5, color='red')
    x2 = min_flops/ peak_membdw
    y2 = peak_membdw * x2
    if x2 > x1:
        '''
        for this case:  -------
                        \  * x
                         \  x *
                          \ * x
        '''
        x2 = peak_flops / peak_membdw - 0.1
        y2 = (peak_flops / peak_membdw)*x2
    print('x1:', x1, ' y1:', y1, ' x2:', x2, ' y2:', y2)
    #ax.plot([x1, x2], [y1, y2], linewidth=1.5, color='red')
    ax.plot([0.1, x1], [peak_membdw*0.1, y1], linewidth=1.5, color='red')

    ax.set_yscale('log')
    ax.set_xscale('log')
    #plt.xscale('log', basex=2)
    #plt.yscale('log', basey=2)
    ax.set_ylabel('GFLOps/sec', fontsize=10)
    ax.set_xlabel('Operational Intensity (FLOps/Byte)', fontsize=10)

    handles, labels = ax.get_legend_handles_labels()
    #print(labels)
    labels_od = OrderedDict(zip(labels, handles))
    ax.legend(labels_od.values(), labels_od.keys(), loc='upper left')

    plt.show()

def draw_op_roofline(op_data_list, peak_flops, peak_membdw):
    op_type_set = {record[0] for record in op_data_list}
    colors = sns.color_palette("hls", n_colors=len(op_type_set) + 2)
    layer_color_map = {val:i for i, val in enumerate(list(op_type_set))}
    #print(layer_color_map)
    fig, ax = plt.subplots(figsize=(6, 6))

    # 1. plot the <flops, intensity> pairs
    for i in op_data_list:
        op_type, flops, intensity = str(i[0]), i[1], i[2]
        if op_type == 'Convolution' or op_type == 'convolution':
            ax.plot(intensity, flops, 'x',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='x')
        elif op_type == 'InnerProduct':
            ax.plot(intensity, flops, 'v',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='v')
        elif op_type == 'Pooling' or op_type == 'pooling':
            ax.plot(intensity, flops, '*',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='*')
        elif op_type == 'Scale' or op_type == 'scale':
            ax.plot(intensity, flops, 's',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='s')
        elif op_type == 'Eltwise' or op_type == 'element-wise':
            ax.plot(intensity, flops, 'd',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='d')
        elif op_type == 'ReLU' or op_type == 'relu':
            ax.plot(intensity, flops, 'p',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='p')
        elif op_type == 'BatchNorm' or op_type == 'batchnorm':
            ax.plot(intensity, flops, 'o',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='o')
        elif op_type == 'Softmax' or op_type == 'softmax':
            ax.plot(intensity, flops, '+',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='+')
        elif op_type == 'LRN' or op_type == 'lrn':
            ax.plot(intensity, flops, '^',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='^')
        elif op_type == 'GEMV' or op_type == 'gemv':
            ax.plot(intensity, flops, '<',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='<')
        elif op_type == 'GEMM' or op_type == 'gemm':
            ax.plot(intensity, flops, 'P',
                    color=colors[layer_color_map[op_type]], label=op_type, marker='P')

    # 2. plot the roof line
    x1 = peak_flops / peak_membdw
    y1 = peak_flops
    max_op_intensity = max([i[2] for i in op_data_list])
    ax.hlines(y=y1, xmin=x1,
        xmax=max_op_intensity+15, linewidth=1.5, color='red')
    min_flops = min([i[1] for i in op_data_list])
    x2 = min_flops / peak_membdw
    y2 = peak_membdw * x2
    ax.plot([x1, x2], [y1, y2], linewidth=1.5, color='red')

    ax.set_yscale('log')
    ax.set_xscale('log')
    #plt.xscale('log', basex=2)
    #plt.yscale('log', basey=2)
    ax.set_ylabel('GFLOps/sec', fontsize=10)
    ax.set_xlabel('Operational Intensity (FLOps/Byte)', fontsize=10)

    handles, labels = ax.get_legend_handles_labels()
    #print(labels)
    labels_od = OrderedDict(zip(labels, handles))
    ax.legend(labels_od.values(), labels_od.keys(), loc='upper left')

    plt.show()

if __name__ == '__main__':
    # AScend 310: 51.2 GB/s, 8 TFLOPS fp16
    ascend310_peak_flops = 8*1000*4
    ascend310_peak_mem_bandwidth = 51.2*4

    ascend310_op_data = extract_op_data('ascend310_op_throughput.txt')
    draw_op_roofline(ascend310_op_data, ascend310_peak_flops, ascend310_peak_mem_bandwidth)
    ascend310_model_data = extract_model_throughput('ascend310_model_throughput.txt')
    draw_model_roofline(ascend310_model_data, ascend310_peak_flops, ascend310_peak_mem_bandwidth)
