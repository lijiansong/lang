import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import numpy as np

# valid_mem_access_dict: key is block_id, value is a tuple of
# (block type, memory addr, block_size, access time interval)
def print_valid_mem_access_info(valid_mem_access_dict):
    for k in valid_mem_access_dict:
        v = valid_mem_access_dict[k]
        print('Block: {} access {} times:'.format(k, len(v)))
        for i in v:
            print(i)

def dump2file_valid_mem_access_info(valid_mem_access_dict):
    with open('valid_mem_access.txt', 'w') as mem_access_writer:
        for k in valid_mem_access_dict:
            v = valid_mem_access_dict[k]
            for i in v:
                # dump access time interval and size(in KB) into file
                time_interval, size = i[-1], i[-2]
                mem_access_writer.write(str(i[-1])+','+str(size)+'\n')


def extract_and_plot(log_file_name,
                     net_name,
                     time_scale=1000.0,
                     mem_scale=1024.0):
    # 1. extract the malloc & free memory behaviours.
    with open(log_file_name, 'r') as mem_info_reader:
        info_list = mem_info_reader.readlines()
        # malloc_free_dict, key is the mem ptr, value is a tupple of
        # ([mem_start_addr], [malloc_size], [malloc_time_stamp], [free_time_stamp])
        malloc_free_dict = {}
        # read_write_dict, key is the mem ptr, value is a tupple of
        # ([read or write], [mem_start_addr], [time_stamp])
        read_write_dict = {}
        start_mem_addr = 0
        # maintain the lex order of the original logs.
        for info in info_list:
            info = info.rstrip('\n')
            #print(info)
            it_list = info.split(' ')
            # 'MALLOC: 0x7f3f8c000000 500000 1617086242333'
            if it_list[0] == 'MALLOC:':
                addr_key = it_list[1]
                mem_addr = int(it_list[1], 16) / mem_scale
                malloc_size = float(it_list[2]) / mem_scale
                malloc_time_stamp = int(it_list[3]) / time_scale
                if addr_key in malloc_free_dict:
                    print('Malloc multiple times! ==> {}: {}, {}, {}'.format(
                            addr_key, mem_addr, malloc_size, malloc_time_stamp))
                    malloc_free_dict[addr_key][0].append(mem_addr)
                    malloc_free_dict[addr_key][1].append(malloc_size)
                    malloc_free_dict[addr_key][2].append(malloc_time_stamp)
                else:
                    malloc_free_dict[addr_key] = ([mem_addr], [malloc_size],
                                               [malloc_time_stamp], [])
            if it_list[0] == 'READ-WRITE:':
                # 'READ-WRITE: 0x55ebcbeff300 1617086242212'
                mem_addr = int(it_list[1], 16) / mem_scale
                time_stamp = int(it_list[2]) / time_scale
                if it_list[1] in read_write_dict:
                    read_write_dict[it_list[1]][0].append('READ-WRITE')
                    read_write_dict[it_list[1]][1].append(mem_addr)
                    read_write_dict[it_list[1]][2].append(time_stamp)
                else:
                    read_write_dict[it_list[1]] = (['READ-WRITE'], [mem_addr], [time_stamp])
            if it_list[0] == 'READ:':
                # 'READ: 0x7f3f8c000000 1617086242333'
                mem_addr = int(it_list[1], 16) / mem_scale
                time_stamp = int(it_list[2]) / time_scale
                if it_list[1] in read_write_dict:
                    read_write_dict[it_list[1]][0].append('READ')
                    read_write_dict[it_list[1]][1].append(mem_addr)
                    read_write_dict[it_list[1]][2].append(time_stamp)
                else:
                    read_write_dict[it_list[1]] = (['READ'], [mem_addr], [time_stamp])

            if it_list[0] == 'FREE:':
                # 'FREE: 0x7f3f8c07a700 1617086242627'
                free_time_stamp = int(it_list[2]) / time_scale
                if it_list[1] in malloc_free_dict:
                    malloc_free_dict[it_list[1]][3].append(free_time_stamp)
                else:
                    print('===> !!!FREE before!!!{}:{}'.format(
                        (int(it_list[1], 16) - start_mem_addr) / mem_scale,
                        free_time_stamp))
        print('malloc_free_dict len: {}'.format(len(malloc_free_dict)))
        print('read_write_dict len: {}'.format(len(read_write_dict)))

    # 2. fill out the invalid info
    # malloc_free_dict, key is the mem ptr, value is a tupple of
    # ([mem_start_addr], [malloc_size], [malloc_time_stamp], [free_time_stamp])
    # valid_mem_list: a list of tuple of (x, y, width, height)
    # (start malloc time, start mem addr, lifetime, malloc size)
    valid_mem_list = []
    block_id = 0
    # valid_block_dict, key is block id, value is a tuple of
    # (start_mem_addr, malloc size, malloc time stamp, free time stamp)
    valid_block_dict = {}
    block_id_map = {}
    for k in malloc_free_dict:
        v = malloc_free_dict[k]
        print('len v[0]: {}, v[1]: {}, v[2]: {}, v[3]: {}'.format(
            len(v[0]), len(v[1]), len(v[2]), len(v[3])))
        min_len = min(len(v[0]), len(v[1]), len(v[2]), len(v[3]))
        if min_len > 0:
            for i in range(min_len):
                start_mem_addr = v[0][i]
                malloc_size = v[1][i]
                malloc_time_stamp = v[2][i]
                free_time_stamp = v[3][i]
                valid_block_dict[block_id] = (start_mem_addr, malloc_size, malloc_time_stamp, free_time_stamp)
                if k in block_id_map:
                    block_id_map[k].append(block_id)
                else:
                    block_id_map[k] = [block_id]
                block_id += 1
    print('valid_block_dict meta block info len: {}'.format(len(valid_block_dict)))
    # valid_mem_access_dict: key is block_id, value is a tuple of
    # (memory addr, block_size, access time interval)
    valid_mem_access_dict = {}
    # for read_write_dict, key is the mem ptr, value is a tuple of
    # ([read or write], [mem_start_addr], [time_stamp])
    for k in read_write_dict:
        # skip current block
        if k not in block_id_map:
            print('{} not in malloc free list!!!'.format(k))
            continue
        v = read_write_dict[k]
        prev_access_time_stamp = v[2][0]
        # start from the second line
        for i, rw in enumerate(v[0][1:]):
            current_mem_start_addr = v[1][i+1]
            current_time_stamp = v[2][i+1]
            time_interval = current_time_stamp - prev_access_time_stamp
            # find out which block id current block belongs to
            for blk_id in block_id_map[k]:
                start_mem_addr = valid_block_dict[blk_id][0]
                malloc_size = valid_block_dict[blk_id][1]
                malloc_time_stamp = valid_block_dict[blk_id][2]
                free_time_stamp = valid_block_dict[blk_id][3]
                if start_mem_addr == current_mem_start_addr and \
                        current_time_stamp >= malloc_time_stamp and \
                        current_time_stamp <= free_time_stamp:
                    #if time_interval >= 200.0:
                    #    print('---> {}, {}'.format(k, read_write_dict[k]))
                    # get it, we need to record the block info.
                    if blk_id in valid_mem_access_dict:
                        valid_mem_access_dict[blk_id].append((current_mem_start_addr, malloc_size, time_interval))
                    else:
                        valid_mem_access_dict[blk_id] = [(current_mem_start_addr, malloc_size, time_interval)]
                    break
            prev_access_time_stamp = current_time_stamp
    print('malloc_free_dict len: {}'.format(len(malloc_free_dict)))
    print('read_write_dict len: {}'.format(len(read_write_dict)))
    print('valid_block_dict meta block info len: {}'.format(len(valid_block_dict)))
    print('valid_mem_access_dict len: {}'.format(len(valid_mem_access_dict)))
    print_valid_mem_access_info(valid_mem_access_dict)
    dump2file_valid_mem_access_info(valid_mem_access_dict)

    # 3. plot cdf for access time_interval of each memory block.
    #time_interval_list = [it[-1] for k, v in valid_mem_access_dict.items() for it in v]
    time_interval_list = []
    for k, v in valid_mem_access_dict.items():
        for it in v:
            # access time interval less than 500.0 us.
            if it[-1] <= 500.0:
                time_interval_list.append(it[-1])

    print('time_interval_list len: {}'.format(len(time_interval_list)))
    plt.subplot(121)
    x, y = sorted(time_interval_list), np.arange(len(time_interval_list)) / len(time_interval_list)
    plt.plot(x, y, color = 'blue', linewidth = 1.0, linestyle = '--')
    plt.xlabel('Access time interval(/us)')
    plt.ylabel('CDF')
    plt.show()

    # 4. plot cdf for memory block size of each memory block.
    block_size_list = [it[-2] for k, v in valid_mem_access_dict.items() for it in v]
    x, y = sorted(block_size_list), np.arange(len(block_size_list)) / len(block_size_list)
    plt.plot(x, y, color = 'blue', linewidth = 1.0, linestyle = '--')
    plt.xlabel('Memory block size(/KB)')
    plt.show()

    block_size_counter = {}
    for size in block_size_list:
        if size in block_size_counter:
            block_size_counter[size] += 1
        else:
            block_size_counter[size] = 1
    print(block_size_counter)
    print(len(block_size_counter))

if __name__ == '__main__':
    #extract_and_plot('knn-mem-info.log', 'kNN')
    #extract_and_plot('lr-mem-info.log', 'Logistic')
    #extract_and_plot('kmeans-mem-info.log', 'KMeans')
    #extract_and_plot('gbdt-mem-info.log', 'GBDT')
    #extract_and_plot('ae-mem-info.log', 'Auto-Encoder')
    #extract_and_plot('bi-rnn-mem-info.log', 'Bi-RNN')
    #extract_and_plot('dyn-rnn-mem-info.log', 'Dynamic-RNN')
    #extract_and_plot('lstm-mem-info.log', 'LSTM')
    extract_and_plot('gan-mem-info.log', 'DCGAN')
    #extract_and_plot('res-mem-info.log', 'ResNet')
