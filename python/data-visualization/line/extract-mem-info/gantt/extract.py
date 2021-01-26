import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import random


def extract_and_plot(log_file_name,
                     net_name,
                     time_scale=1000.0,
                     mem_scale=1024.0):
    # 1. extract the malloc & free memory behaviours.
    with open(log_file_name, 'r') as mem_info_reader:
        info_list = mem_info_reader.readlines()
        # malloc_dict, key is the mem ptr, value is a tupple of
        # ([mem_start_addr], [malloc_size], [malloc_time_stamp], [free_time_stamp])
        malloc_dict = {}
        start_mem_addr = 0
        start_time_stamp = 0
        counter = 0
        max_mem_addr = 0
        max_free_time = 0
        for info in info_list:
            info = info.rstrip('\n')
            #print(info)
            #MALLOC: 0x7f7db6008200 4 1602580526755720327
            #FREE: 0x7f7db6003200 1602580526794718008
            it_list = info.split(' ')
            if counter == 0:
                # extract the start memory address & start time stamp
                start_time_stamp = int(it_list[3])
                start_mem_addr = int(it_list[1], 16)
            else:
                if it_list[0] == 'MALLOC:':
                    # in KB
                    mem_addr = (int(it_list[1], 16) -
                                start_mem_addr) / mem_scale
                    malloc_size = float(it_list[2]) / mem_scale
                    max_mem_addr = max(max_mem_addr, mem_addr + malloc_size)
                    # in ms
                    malloc_time_stamp = (int(it_list[3]) -
                                         start_time_stamp) / time_scale
                    if it_list[1] in malloc_dict:
                        print(
                            'Malloc multiple times! ==> {}: {}, {}, {}'.format(
                                it_list[1], mem_addr, malloc_size,
                                malloc_time_stamp))
                        malloc_dict[it_list[1]][0].append(mem_addr)
                        malloc_dict[it_list[1]][1].append(malloc_size)
                        malloc_dict[it_list[1]][2].append(malloc_time_stamp)
                    else:
                        malloc_dict[it_list[1]] = ([mem_addr], [malloc_size],
                                                   [malloc_time_stamp], [])
                if it_list[0] == 'FREE:':
                    free_time_stamp = (int(it_list[2]) -
                                       start_time_stamp) / time_scale
                    if it_list[1] in malloc_dict:
                        malloc_dict[it_list[1]][3].append(free_time_stamp)
                    else:
                        print('===> !!!FREE before!!!{}:{}'.format(
                            (int(it_list[1], 16) - start_mem_addr) / mem_scale,
                            free_time_stamp))
                    max_free_time = max(max_free_time, free_time_stamp)
            counter += 1
        print('---> {}'.format(len(malloc_dict)))
        #print(malloc_dict)
        print('---> max_mem_addr: {}'.format(max_mem_addr))
        print('---> max_free_time: {}'.format(max_free_time))
    # 2. fill out the invalid info
    # malloc_dict, key is the mem ptr, value is a tupple of
    # ([mem_start_addr], [malloc_size], [malloc_time_stamp], [free_time_stamp])
    # valid_mem_list: a list of tuple of (x, y, width, height)
    # (start malloc time, start mem addr, lifetime, malloc size)
    max_mem_addr = 0
    valid_mem_list = []
    for k in malloc_dict:
        # go through the [mem_start_addr]
        v = malloc_dict[k]
        print('len v[0]: {}, v[1]: {}, v[2]: {}, v[3]: {}'.format(
            len(v[0]), len(v[1]), len(v[2]), len(v[3])))
        min_len = min(len(v[0]), len(v[1]), len(v[2]), len(v[3]))
        if min_len > 0:
            for i in range(min_len):
                start_malloc_time = v[2][i]
                start_mem_addr = v[0][i]
                malloc_size = v[1][i]
                max_mem_addr = max(max_mem_addr, start_mem_addr + malloc_size)
                lifetime = v[3][i] - v[2][i]
                #print('--> {}, {}: {}'.format(i, k, v))
                valid_mem_list.append(
                    (start_malloc_time, start_mem_addr, lifetime, malloc_size))
    #print(valid_mem_list)

    x0_start_malloc_time = valid_mem_list[0][0]
    y0_start_mem_addr = valid_mem_list[0][1]

    # 3. plot valid_mem_list
    colors = sns.color_palette("hls", n_colors=len(valid_mem_list) + 10)
    random_color_list = list(set(random.sample(range(len(valid_mem_list) + 10), len(valid_mem_list))))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_ylabel('Normalized memory address', fontsize=15)
    ax.set_xlabel('Normalized time stamp', fontsize=15)
    #plt.title(net_name)
    '''
    :                +------------------+
    :                |                  |
    :              height               |
    :                |                  |
    :             (x, y)---- width -----+
    '''
    for i, data in enumerate(valid_mem_list):
        start_malloc_time, start_mem_addr, lifetime, malloc_size = data[
            0], data[1], data[2], data[3]
        x = (start_malloc_time - x0_start_malloc_time) / max_free_time
        y = (start_mem_addr - y0_start_mem_addr) / max_mem_addr
        width = lifetime / max_free_time
        height = malloc_size / max_mem_addr
        ax.add_patch(patches.Rectangle((x, y), width, height, color=colors[random_color_list[i]]))
    plt.show()


if __name__ == '__main__':
    extract_and_plot('mlp-mem-info.log', 'MLP')
    #extract_and_plot('alexnet-mem-info.log', 'AlexNet')
    #extract_and_plot('resnet-mem-info.log', 'ResNet')
    #extract_and_plot('rnn-mem-info.log', 'RNN')
    #extract_and_plot('xception-mem-info.log', 'Xception')
    #extract_and_plot('gan-graph-mode-mem-info.log', 'GAN')
    #extract_and_plot('gan-seq-mode-mem-info.log', 'GAN')
