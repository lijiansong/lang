from mpl_toolkits import mplot3d

import numpy as np
import matplotlib.pyplot as plt

def plot_3d_scatter(x_data, y_data, z_data, x_label, y_label, z_label):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel(x_label)
    #ax.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax.set_ylabel(y_label)
    #ax.set_yticks([1, 2, 4, 8, 16, 32])
    ax.set_zlabel(z_label)

    #ax.scatter3D(tn_list, dp_list, end2end_list, c=end2end_list, cmap='Greens');
    if 'hardware' in z_label:
        ax.scatter3D(x_data, y_data, z_data, c='r', marker='o', label=z_label, s=10);
    else:
        ax.scatter3D(x_data, y_data, z_data, c='g', marker='^', label=z_label, s=10);

    #ax.legend(loc='best')

    plt.show()

def plot_combine_scatter(tn_list, dp_list, end2end_list, hw_list):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('thread number')
    #ax.set_xticks([1, 2, 4, 8, 16, 32, 64])
    ax.set_ylabel('data parallelism')
    #ax.set_yticks([1, 2, 4, 8, 16, 32])
    ax.set_zlabel('FPS')

    ax.scatter3D(tn_list, dp_list, end2end_list, c='g', marker='+', label='end-to-end FPS', s=20);
    ax.scatter3D(tn_list, dp_list, hw_list, c='r', marker='^', label='hardware FPS', s=10);
    ax.legend(loc='best')

    plt.show()

def extract_data(data_file_name):
    tn_list = []
    dp_list = []
    end2end_list = []
    hw_list = []
    with open(data_file_name, 'r') as f:
        line_list = f.readlines()
        for line in line_list:
            line = line.strip().split('\t')
            dp, tn, end2end, hw = int(line[0]), int(line[1]), float(line[2]), float(line[3])
            tn_list.append(tn)
            dp_list.append(dp)
            end2end_list.append(end2end)
            hw_list.append(hw)
    return tn_list, dp_list, end2end_list, hw_list

if __name__ == '__main__':
    #tn_list, dp_list, end2end_list, hw_list = extract_data('mobilenet-data.txt')
    tn_list, dp_list, end2end_list, hw_list = extract_data('resnet-data.txt')
    plot_3d_scatter(tn_list, dp_list, end2end_list, 'thread number', 'data parallelism', 'end-to-end FPS')
    plot_3d_scatter(tn_list, dp_list, hw_list, 'thread number', 'data parallelism', 'hardware FPS')
    plot_combine_scatter(tn_list, dp_list, end2end_list, hw_list)
