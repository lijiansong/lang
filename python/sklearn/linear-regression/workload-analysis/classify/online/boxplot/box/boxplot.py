import matplotlib.pyplot as plt
import matplotlib.colors as mc
import numpy as np
import pandas as pd
import collections
import seaborn as sns
from pandas import ExcelWriter
from pandas import ExcelFile
import colorsys

def extract_data(file_name, network_list=['MobileNetV1', 'SqueezeNet', 'DenseNet121', 'ResNet50', 'SSD_MobileNetV1', 'SSD_VGG16']):
    file_reader = open(file_name, 'r')
    # dense-fp16, dense-int8
    res_list = [[] for _ in range(len(network_list)*2)]

    type_list = []
    throughput_list = []
    net_list=[]
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        for line in text_lines:
            line = line.rstrip('\n').split('\t')
            #print(line)
            for i, item in enumerate(line):
                if item != '':
                    res_list[i].append(float(item))
        print(res_list)
        print(len(res_list))
        total = 0
        for i, end2end_throughput_list in enumerate(res_list):
            total += len(end2end_throughput_list)
            if i % 2 == 0:
                print('dense-fp16:', network_list[i // 2])
                for throughput in end2end_throughput_list:
                    throughput_list.append(throughput)
                    net_list.append(network_list[i // 2])
                    type_list.append('FP16')
            elif i % 2 == 1:
                print('dense-int8:', network_list[i // 2])
                for throughput in end2end_throughput_list:
                    throughput_list.append(throughput)
                    net_list.append(network_list[i // 2])
                    type_list.append('INT8')
            print('Expected:', total, 'Acutal:', len(type_list))
    finally:
        if file_reader:
            file_reader.close()
    return net_list, type_list, throughput_list

def lighten_color(color, amount=0.5):
    # --------------------- SOURCE: @IanHincks ---------------------
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])

def plot_box(end2end_or_hw, net_list, type_list, throughput_list):
    od = collections.OrderedDict()
    od['net'] = net_list
    od['type'] = type_list
    throughput_key = ''
    if 'end2end' in end2end_or_hw:
        throughput_key = 'End-to-end FPS'
        od[throughput_key] = throughput_list
    else:
        throughput_key = 'Hardware FPS'
        od[throughput_key] = throughput_list

    df = pd.DataFrame(od)

    plt.figure(figsize=(10,8))
    if 'end2end' in end2end_or_hw:
        ax = sns.boxplot(x="net", hue="type", y=throughput_key, data=df, palette="Set3", linewidth=1, showfliers = False)
    else:
        ax = sns.boxplot(x="net", hue="type", y=throughput_key, data=df, palette="Set3", linewidth=1, showfliers = False)
    ax.yaxis.grid(True)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30)
    ax.set_ylabel(throughput_key, fontsize=20)
    plt.setp(ax.get_legend().get_texts(), fontsize='30')
    #for i, artist in enumerate(ax.artists):
    #    # Set the linecolor on the artist to the facecolor, and set the facecolor to None
    #    col = lighten_color(artist.get_facecolor(), 1.2)
    #    artist.set_edgecolor(col)
    plt.show()

if __name__ == '__main__':
    e2e_net_list, e2e_type_list, e2e_throughput_list = extract_data('end2end-throughput.txt')
    plot_box('end2end', e2e_net_list, e2e_type_list, e2e_throughput_list)
    hw_net_list, hw_type_list, hw_throughput_list = extract_data('hardware-throughput.txt')
    plot_box('hw', hw_net_list, hw_type_list, hw_throughput_list)

