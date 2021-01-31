import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

def extract_data(data_file_blob='data.txt'):
    data_list = []
    with open(data_file_blob, 'r') as f:
        data_lines = f.readlines()
        for data in data_lines:
            data = data.rstrip('\n')
            value = float(data)
            if value >= 50.0:
                continue
            else:
                data_list.append(value)

    return data_list

def violin_plot(data_list):
    print(data_list)
    ax = sns.violinplot(x=data_list)
    ax.set_xlabel('Access time interval(/us)')
    plt.show()


if __name__ == '__main__':
    data_list = extract_data('mlp-data.txt')
    violin_plot(data_list)
