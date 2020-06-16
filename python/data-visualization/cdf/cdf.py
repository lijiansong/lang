from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

'''
REF: https://stackoverflow.com/questions/3209362/how-to-plot-empirical-cdf-in-matplotlib-in-python
'''
'''
data=[14.27,14.80,12.28,17.09,15.10,12.92,15.56,15.38,
      15.15,13.98,14.90,15.91,14.52,15.63,13.83,13.66,
      13.98,14.47,14.65,14.73,15.18,14.49,14.56,15.03,
      15.40,14.68,13.33,14.41,14.19,15.21,14.75,14.41,
      14.04,13.68,15.31,14.32,13.64,14.77,14.30,14.62,
      14.10,15.47,13.73,13.65,15.02,14.01,14.92,15.47,
      13.75,14.87,15.28,14.43,13.96,14.57,15.49,15.13,
      14.23,14.44,14.57]
plt.subplot(121)
hist, bin_edges = np.histogram(data)
cdf = np.cumsum(hist)
plt.plot(bin_edges[1:], cdf)

plt.show()
'''

def extract_data(data_path):
    data_list = []
    with open(data_path, 'r') as f:
        data_lines = f.readlines()
        for line in data_lines:
            data_list.append(float(line))
    return data_list

def draw_cdf(data):
    plt.subplot(121)
    #hist, bin_edges = np.histogram(data, normed=True)
    #cdf = np.cumsum(hist)
    #plt.plot(bin_edges[1:], cdf)

    #plt.hist(data, normed=True, cumulative=True, label='CDF',
    #     histtype='step', alpha=0.8, color='k')

    x, y = sorted(data), np.arange(len(data)) / len(data)
    l1 = plt.plot(x, y, label = 'MobileNetV1', color = 'red', linewidth = 1.0, linestyle = '--')
    plt.xlabel('End-to-end FPS')
    plt.legend(handles = [l1], labels = ['MobileNetV1'], loc = 'best')
    plt.show()

if __name__ == '__main__':
    end2end_fps_data = extract_data('mobilenet-end2end-fps.txt')
    draw_cdf(end2end_fps_data)

