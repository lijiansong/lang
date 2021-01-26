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


def extract_block_type(type_info_log):
    # block_info_map key is the memory address, value is a set of block type,
    # since the high-level framework usually performs some memory optimizations.
    block_info_map = {}
    with open(type_info_log, 'r') as log_reader:
        info_list = log_reader.readlines()
        for info in info_list:
            info = info.rstrip('\n')
            if info[0] == '%':
                continue
            it_list = info.split(' ')
            mem_addr, blk_type = it_list[0], it_list[1]
            if mem_addr in block_info_map:
                # FIXME:check blk_type
                block_info_map[mem_addr].add(blk_type)
            else:
                block_info_map[mem_addr] = set({blk_type})
    print(block_info_map)
    print(len(block_info_map))
    return block_info_map


def extract_and_plot(block_type_map,
                     log_file_name,
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
        # ([read or write], [mem_start_addr], [block_size], [time_stamp])
        read_write_dict = {}
        start_mem_addr = 0
        # maintain the lex order of the original logs.
        for info in info_list:
            info = info.rstrip('\n')
            #print(info)
            it_list = info.split(' ')
            # 'MALLOC: 0x7f7db6008200 4 1602580526755720327'
            # 'MALLOC: Type: Inter 0x7f8c4e005c00 3200 1602941501356865290'
            if it_list[0] == 'MALLOC:':
                if it_list[1] == 'Type:':
                    addr_key = it_list[3]
                    mem_addr = int(it_list[3], 16) / mem_scale
                    malloc_size = float(it_list[4]) / mem_scale
                    malloc_time_stamp = int(it_list[5]) / time_scale
                else:
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
            if it_list[0] == 'WRITE:':
                # 'WRITE: 0x7f76ee001e00 4800 1602759703270048403'
                mem_addr = int(it_list[1], 16) / mem_scale
                block_size = float(it_list[2]) / mem_scale
                time_stamp = int(it_list[3]) / time_scale
                if it_list[1] in read_write_dict:
                    read_write_dict[it_list[1]][0].append('WRITE')
                    read_write_dict[it_list[1]][1].append(mem_addr)
                    read_write_dict[it_list[1]][2].append(block_size)
                    read_write_dict[it_list[1]][3].append(time_stamp)
                else:
                    read_write_dict[it_list[1]] = (['WRITE'], [mem_addr], [block_size], [time_stamp])
            if it_list[0] == 'READ:':
                # 'READ: 0x7f76ee003200 1600 1602759703270058576'
                mem_addr = int(it_list[1], 16) / mem_scale
                block_size = float(it_list[2]) / mem_scale
                time_stamp = int(it_list[3]) / time_scale
                if it_list[1] in read_write_dict:
                    read_write_dict[it_list[1]][0].append('READ')
                    read_write_dict[it_list[1]][1].append(mem_addr)
                    read_write_dict[it_list[1]][2].append(block_size)
                    read_write_dict[it_list[1]][3].append(time_stamp)
                else:
                    read_write_dict[it_list[1]] = (['READ'], [mem_addr], [block_size], [time_stamp])

            if it_list[0] == 'FREE:':
                # 'FREE: 0x7f7db6003200 1602580526794718008'
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
        #print('len v[0]: {}, v[1]: {}, v[2]: {}, v[3]: {}'.format(
        #    len(v[0]), len(v[1]), len(v[2]), len(v[3])))
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
    # (block type, memory addr, block_size, access time interval)
    valid_mem_access_dict = {}
    # for read_write_dict, key is the mem ptr, value is a tuple of
    # ([read or write], [mem_start_addr], [block_size], [time_stamp])
    for k in read_write_dict:
        # skip current block
        if k not in block_id_map or k not in block_type_map:
            continue
        block_type = list(block_type_map[k])[0]
        v = read_write_dict[k]
        prev_access_time_stamp = v[3][0]
        # start from the second line
        for i, rw in enumerate(v[0][1:]):
            current_mem_start_addr = v[1][i+1]
            current_block_size = v[2][i+1]
            current_time_stamp = v[3][i+1]
            time_interval = current_time_stamp - prev_access_time_stamp
            # find out which block id current block belongs to
            for blk_id in block_id_map[k]:
                start_mem_addr = valid_block_dict[blk_id][0]
                malloc_size = valid_block_dict[blk_id][1]
                malloc_time_stamp = valid_block_dict[blk_id][2]
                free_time_stamp = valid_block_dict[blk_id][3]
                if start_mem_addr == current_mem_start_addr and \
                        malloc_size == current_block_size and \
                        current_time_stamp >= malloc_time_stamp and \
                        current_time_stamp <= free_time_stamp:
                    #if time_interval >= 200.0:
                    #    print('---> {}, {}'.format(k, read_write_dict[k]))
                    # get it, we need to record the block info.
                    if blk_id in valid_mem_access_dict:
                        valid_mem_access_dict[blk_id].append((block_type, current_mem_start_addr, current_block_size, time_interval))
                    else:
                        valid_mem_access_dict[blk_id] = [(block_type, current_mem_start_addr, current_block_size, time_interval)]
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
    blk_info_map = extract_block_type('large-logs/block-type-info.log')
    extract_and_plot(blk_info_map, 'large-logs/mem-info.log', 'MLP')
    #blk_info_map = extract_block_type('block-type-info.log')
    #extract_and_plot(blk_info_map, 'mem-info.log', 'MLP')
    #blk_info_map = extract_block_type('mlp-small-logs/block-type-info.log')
    #extract_and_plot(blk_info_map, 'mlp-small-logs/mem-info.log', 'MLP')
