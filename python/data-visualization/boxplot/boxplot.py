import matplotlib.pyplot as plt
import numpy as np

def get_data(file_name, network_list=['MobileNet', 'SqueezeNet', 'DenseNet121', 'ResNet50']):
    file_reader = open(file_name, 'r')
    res_list = [[] for _ in network_list]
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        for line in text_lines:
            line = line.rstrip('\n').split('\t')
            #print(line)
            for i, item in enumerate(line):
                if item != '':
                    res_list[i].append(float(item))
        #print(res_list)
    finally:
        if file_reader:
            file_reader.close()
    return res_list

def plot_box(data_list, labels_list=['MobileNet', 'SqueezeNet', 'DenseNet121', 'ResNet50']):
    bplot = plt.boxplot(data_list, patch_artist=True, labels=labels_list, showfliers=False)
    colors = ['pink', 'lightblue', 'lightgreen', 'lightyellow']
    for patch, color in zip(bplot['boxes'], colors):
        patch.set_facecolor(color)
    plt.gca().yaxis.grid(True)
    plt.ylabel('End to end FPS')
    plt.show()

if __name__ == '__main__':
    data = get_data('data/end2end-fps.txt')
    #data = get_data('data/hardware-fps.txt')
    plot_box(data)
