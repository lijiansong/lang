import matplotlib.pyplot as plt

def extract_data(file_blob='swapinout-ns.txt'):
    size_list, in_time_list, out_time_list = [], [], []
    with open('swapinout-ns.txt', 'r') as f:
        data_list = f.readlines()
        for data in data_list:
            data=data.rstrip('\n')
            size, in_time, out_time=data.split(',')
            size_list.append(int(size))
            in_time_list.append(int(in_time))
            out_time_list.append(int(out_time))
    return size_list, in_time_list, out_time_list

def plot_points(size_list, in_time_list, out_time_list):
    plt.xscale('log')
    plt.yscale('log')
    plt.plot(size_list, in_time_list, 'g^')
    plt.ylabel('swapping latency(/ns)', fontsize=18)
    plt.xlabel('host to device swap-in bytes', fontsize=18)
    plt.show()

    plt.xscale('log')
    plt.yscale('log')
    plt.plot(size_list, out_time_list, 'bs')
    #plt.plot(size_list, out_time_list, 'bo')
    plt.ylabel('swapping latency(/ns)', fontsize=18)
    plt.xlabel('device to host swap-out bytes', fontsize=18)
    plt.show()

if __name__ == '__main__':
    size_list, in_time_list, out_time_list = extract_data()
    plot_points(size_list, in_time_list, out_time_list)
