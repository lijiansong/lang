import matplotlib.pyplot as plt
from collections import OrderedDict
import seaborn as sns

def extract_plot(data_file_blob='data.txt', outlier=100.0):
    # 1. extract data.
    access_time_interval_list, blk_size_list = [], []
    with open(data_file_blob, 'r') as f:
        data_lines = f.readlines()
        for data in data_lines:
            data = data.rstrip('\n')
            items = data.split(',')
            _ati, _size = float(items[0]), float(items[1])
            access_time_interval_list.append(_ati)
            # FIXME: only scale for GBDT in tf internal logs
            if 'gbdt' in data_file_blob:
                blk_size_list.append(_size/100.0)
            else:
                blk_size_list.append(_size/1000.0)

    # 2. scatter plot.
    fig, ax1 = plt.subplots()
    y1_color = 'tab:red'
    ax1.set_ylabel('Access time intervals(/us)', color=y1_color)
    x_list=[i for i in range(len(access_time_interval_list))]
    #ax1.plot(x_list, access_time_interval_list, 'x', color=y1_color, label='ATIs')
    #ax1.plot(x_list, access_time_interval_list, '-p', color=y1_color, label='ATIs')
    ax1.plot(x_list, access_time_interval_list, 'p', color=y1_color, label='ATIs')
    ax1.tick_params(axis='y', labelcolor=y1_color)

    # instantiate a second axes that shares the same x-axis
    ax2 = ax1.twinx()
    y2_color = 'tab:blue'
    ax2.set_ylabel('Memory block size(/MB)', color=y2_color)
    #ax2.plot(x_list, blk_size_list, '+', color=y2_color)
    ax2.plot(x_list, blk_size_list, '.', color=y2_color, label='block size')
    ax2.tick_params(axis='y', labelcolor=y2_color)

    fig.tight_layout()
    plt.show()

    # violin plot
    valid_ati_list = list(filter(lambda x: x < outlier, access_time_interval_list))
    ax = sns.violinplot(x=valid_ati_list, orient='h')
    ax.set_xlabel('Access time interval(/us)')
    plt.show()

if __name__ == '__main__':
    #extract_plot('knn-data.txt', 100.0)
    #extract_plot('kmeans-data.txt', 80.0)
    #extract_plot('log-regr-data.txt', 50.0)
    extract_plot('gbdt-data.txt', 100.0)
