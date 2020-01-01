#!/usr/bin/env python3

def get_bs_vs_tn(in_file_name, out_file_name, best_config_list):
    '''
    Note: best case for dense int8 new log is:
        batch_size  data_parallel   model_parallel   thread_num
        16	4	1	8

    batch size:     1 2 4 8 16 32 64 128 256 512 1024
    data parallel:  1 2 4 8 16 32
    model parallel: 1 2 4 8 16 32
    thread num:     1 2 4 8 16 32 64 128

    for 'batch size' vs 'thread num': 11 x 8
    '''
    best_bs, best_dp, best_mp, best_tn = best_config_list[0], best_config_list[1], best_config_list[2], best_config_list[3]
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:9, 512:10, 1024:11}
    #thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8}
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    data_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    model_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    file_reader = open(in_file_name, 'r')
    file_writer = open(out_file_name, 'w')
    res_list = [None for _ in range(len(batch_size_index_dict)*len(thread_num_index_dict))]
    try:
        text_lines = file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            if model_parallel == best_mp and data_parallel == best_dp:
                index = (batch_size_index_dict[batch_size] - 1) * len(thread_num_index_dict) + thread_num_index_dict[thread_num] - 1
                res_list[index] = end2end_fps
        print(len(res_list), res_list)
        for i in range(len(batch_size_index_dict)):
            res_str = ''
            for j in range(len(thread_num_index_dict)):
                if j == len(thread_num_index_dict) - 1:
                    if res_list[i * len(thread_num_index_dict) + j] == None:
                        res_str += '\n'
                    else:
                        res_str += str(res_list[i * len(thread_num_index_dict) + j]) + '\n'
                else:
                    if res_list[i * len(thread_num_index_dict) + j] == None:
                        res_str += ','
                    else:
                        res_str += str(res_list[i * len(thread_num_index_dict) + j]) + ','
            print(res_str)
            file_writer.write(res_str)

    finally:
        if file_reader:
            file_reader.close()
            file_writer.close()

def get_dp_vs_mp(in_file_name, out_file_name, best_config_list):
    '''
    Note: best case for dense int8 new log is:
        batch_size  data_parallel   model_parallel   thread_num
        16	4	1	8

    batch size:     1 2 4 8 16 32 64 128 256 512 1024
    data parallel:  1 2 4 8 16 32
    model parallel: 1 2 4 8 16 32
    thread num:     1 2 4 8 16 32 64 128

    for 'batch size' vs 'thread num': 11 x 8
    '''
    best_bs, best_dp, best_mp, best_tn = best_config_list[0], best_config_list[1], best_config_list[2], best_config_list[3]
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:9, 512:10, 1024:11}
    #thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8}
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    data_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    model_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    file_reader = open(in_file_name, 'r')
    file_writer = open(out_file_name, 'w')
    res_list = [None for _ in range(len(data_parallel_index_dict)*len(model_parallel_index_dict))]
    try:
        text_lines = file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            if batch_size == best_bs and thread_num == best_tn:
                index = (data_parallel_index_dict[data_parallel] - 1) * len(model_parallel_index_dict) + model_parallel_index_dict[model_parallel] - 1
                res_list[index] = end2end_fps
        print(len(res_list), res_list)
        for i in range(len(data_parallel_index_dict)):
            res_str = ''
            for j in range(len(model_parallel_index_dict)):
                if j == len(model_parallel_index_dict) - 1:
                    if res_list[i * len(model_parallel_index_dict) + j] == None:
                        res_str += '\n'
                    else:
                        res_str += str(res_list[i * len(model_parallel_index_dict) + j]) + '\n'
                else:
                    if res_list[i * len(model_parallel_index_dict) + j] == None:
                        res_str += ','
                    else:
                        res_str += str(res_list[i * len(model_parallel_index_dict) + j]) + ','
            print(res_str)
            file_writer.write(res_str)

    finally:
        if file_reader:
            file_reader.close()
            file_writer.close()

def get_heat_map_data(in_file_name, out_file_name, column_opt_dict, row_opt_dict, column_line_map, row_line_map, best_colum, best_row, remain_opt_first, remain_opt_second, best_config_list):
    '''
    Note: best case for dense int8 new log is:
        batch_size  data_parallel   model_parallel   thread_num
        16	4	1	8

    batch size:     1 2 4 8 16 32 64 128 256 512 1024
    data parallel:  1 2 4 8 16 32
    model parallel: 1 2 4 8 16 32
    thread num:     1 2 4 8 16 32 64 128

    for 'batch size' vs 'thread num': 11 x 8
    '''
    best_bs, best_dp, best_mp, best_tn = 16, 4, 1, 8
    best_bs, best_dp, best_mp, best_tn = best_config_list[0], best_config_list[1], best_config_list[2], best_config_list[3]
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:9, 512:10, 1024:11}
    #thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8}
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    data_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    model_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    file_reader = open(in_file_name, 'r')
    file_writer = open(out_file_name, 'w')
    res_list = [None for _ in range(len(column_opt_dict)*len(row_opt_dict))]
    try:
        text_lines = file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            row_key = int(line[column_line_map])
            column_key = int(line[row_line_map])
            if row_key == best_column and column_key == best_row:
                index = (data_parallel_index_dict[data_parallel] - 1) * len(model_parallel_index_dict) + model_parallel_index_dict[model_parallel] - 1
                res_list[index] = end2end_fps
        print(len(res_list), res_list)
        for i in range(len(data_parallel_index_dict)):
            res_str = ''
            for j in range(len(model_parallel_index_dict)):
                if j == len(batch_size_index_dict) - 1:
                    if res_list[i * len(model_parallel_index_dict) + j] == None:
                        res_str += '\n'
                    else:
                        res_str += str(res_list[i * len(model_parallel_index_dict) + j]) + '\n'
                else:
                    if res_list[i * len(model_parallel_index_dict) + j] == None:
                        res_str += ','
                    else:
                        res_str += str(res_list[i * len(model_parallel_index_dict) + j]) + ','
            print(res_str)
            file_writer.write(res_str + '\n')

    finally:
        if file_reader:
            file_reader.close()
            file_writer.close()

def get_bs_vs_dp(in_file_name, out_file_name, best_config_list):
    '''
    Note: best case for dense int8 new log is:
        batch_size  data_parallel   model_parallel   thread_num
        16	4	1	8

    batch size:     1 2 4 8 16 32 64 128 256 512 1024
    data parallel:  1 2 4 8 16 32
    model parallel: 1 2 4 8 16 32
    thread num:     1 2 4 8 16 32 64 128

    for 'batch size' vs 'thread num': 11 x 8
    '''
    best_bs, best_dp, best_mp, best_tn = 16, 4, 1, 8
    best_bs, best_dp, best_mp, best_tn = best_config_list[0], best_config_list[1], best_config_list[2], best_config_list[3]
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:9, 512:10, 1024:11}
    #thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8}
    batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    data_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    model_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    file_reader = open(in_file_name, 'r')
    file_writer = open(out_file_name, 'w')
    res_list = [None for _ in range(len(batch_size_index_dict)*len(data_parallel_index_dict))]
    try:
        text_lines = file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            if model_parallel == best_mp and thread_num == best_tn:
                index = (batch_size_index_dict[batch_size] - 1) * len(data_parallel_index_dict) + data_parallel_index_dict[data_parallel] - 1
                res_list[index] = end2end_fps
        print(len(res_list), res_list)
        for i in range(len(batch_size_index_dict)):
            res_str = ''
            for j in range(len(data_parallel_index_dict)):
                index = i * len(data_parallel_index_dict) + j
                if j == len(data_parallel_index_dict) - 1:
                    if res_list[index] == None:
                        res_str += '\n'
                    else:
                        res_str += str(res_list[index]) + '\n'
                else:
                    if res_list[index] == None:
                        res_str += ','
                    else:
                        res_str += str(res_list[index]) + ','
            print(res_str)
            file_writer.write(res_str)

    finally:
        if file_reader:
            file_reader.close()
            file_writer.close()

def get_bs_vs_mp(in_file_name, out_file_name, best_config_list):
    '''
    Note: best case for dense int8 new log is:
        batch_size  data_parallel   model_parallel   thread_num
        16	4	1	8

    batch size:     1 2 4 8 16 32 64 128 256 512 1024
    data parallel:  1 2 4 8 16 32
    model parallel: 1 2 4 8 16 32
    thread num:     1 2 4 8 16 32 64 128

    for 'batch size' vs 'thread num': 11 x 8
    '''
    best_bs, best_dp, best_mp, best_tn = 16, 4, 1, 8
    best_bs, best_dp, best_mp, best_tn = best_config_list[0], best_config_list[1], best_config_list[2], best_config_list[3]
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:9, 512:10, 1024:11}
    #thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8}
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    data_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    model_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    file_reader = open(in_file_name, 'r')
    file_writer = open(out_file_name, 'w')
    res_list = [None for _ in range(len(batch_size_index_dict)*len(model_parallel_index_dict))]
    try:
        text_lines = file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            if data_parallel == best_dp and thread_num == best_tn:
                index = (batch_size_index_dict[batch_size] - 1) * len(model_parallel_index_dict) + model_parallel_index_dict[model_parallel] - 1
                res_list[index] = end2end_fps
        print(len(res_list), res_list)
        for i in range(len(batch_size_index_dict)):
            res_str = ''
            for j in range(len(model_parallel_index_dict)):
                index = i * len(model_parallel_index_dict) + j
                if j == len(model_parallel_index_dict) - 1:
                    if res_list[index] == None:
                        res_str += '\n'
                    else:
                        res_str += str(res_list[index]) + '\n'
                else:
                    if res_list[index] == None:
                        res_str += ','
                    else:
                        res_str += str(res_list[index]) + ','
            print(res_str)
            file_writer.write(res_str)

    finally:
        if file_reader:
            file_reader.close()
            file_writer.close()

def get_tn_vs_dp(in_file_name, out_file_name, best_config_list):
    '''
    Note: best case for dense int8 new log is:
        batch_size  data_parallel   model_parallel   thread_num
        16	4	1	8

    batch size:     1 2 4 8 16 32 64 128 256 512 1024
    data parallel:  1 2 4 8 16 32
    model parallel: 1 2 4 8 16 32
    thread num:     1 2 4 8 16 32 64 128

    for 'batch size' vs 'thread num': 11 x 8
    '''
    best_bs, best_dp, best_mp, best_tn = best_config_list[0], best_config_list[1], best_config_list[2], best_config_list[3]
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:9, 512:10, 1024:11}
    #thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8}
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    data_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    model_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    file_reader = open(in_file_name, 'r')
    file_writer = open(out_file_name, 'w')
    res_list = [None for _ in range(len(thread_num_index_dict)*len(data_parallel_index_dict))]
    try:
        text_lines = file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            if model_parallel == best_mp and batch_size == best_bs:
                index = (thread_num_index_dict[thread_num] - 1) * len(data_parallel_index_dict) + data_parallel_index_dict[data_parallel] - 1
                res_list[index] = end2end_fps
        print(len(res_list), res_list)
        for i in range(len(thread_num_index_dict)):
            res_str = ''
            for j in range(len(data_parallel_index_dict)):
                index = i * len(data_parallel_index_dict) + j
                if j == len(data_parallel_index_dict) - 1:
                    if res_list[index] == None:
                        res_str += '\n'
                    else:
                        res_str += str(res_list[index]) + '\n'
                else:
                    if res_list[index] == None:
                        res_str += ','
                    else:
                        res_str += str(res_list[index]) + ','
            print(res_str)
            file_writer.write(res_str)

    finally:
        if file_reader:
            file_reader.close()
            file_writer.close()

def get_tn_vs_mp(in_file_name, out_file_name, best_config_list):
    '''
    Note: best case for dense int8 new log is:
        batch_size  data_parallel   model_parallel   thread_num
        16	4	1	8

    batch size:     1 2 4 8 16 32 64 128 256 512 1024
    data parallel:  1 2 4 8 16 32
    model parallel: 1 2 4 8 16 32
    thread num:     1 2 4 8 16 32 64 128

    for 'batch size' vs 'thread num': 11 x 8
    '''
    best_bs, best_dp, best_mp, best_tn = best_config_list[0], best_config_list[1], best_config_list[2], best_config_list[3]
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8, 256:9, 512:10, 1024:11}
    #thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7, 128:8}
    #batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    batch_size_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    thread_num_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6, 64:7}
    data_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    model_parallel_index_dict={1:1, 2:2, 4:3, 8:4, 16:5, 32:6}
    file_reader = open(in_file_name, 'r')
    file_writer = open(out_file_name, 'w')
    res_list = [None for _ in range(len(thread_num_index_dict)*len(model_parallel_index_dict))]
    try:
        text_lines = file_reader.readlines()
        for line in text_lines:
            line = line.rstrip('\n')
            line = line.split('\t')
            batch_size, data_parallel, model_parallel, thread_num, fifo_size, end2end_fps = int(line[0]), int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            if model_parallel == best_mp and batch_size == best_bs:
                index = (thread_num_index_dict[thread_num] - 1) * len(model_parallel_index_dict) + model_parallel_index_dict[model_parallel] - 1
                res_list[index] = end2end_fps
        print(len(res_list), res_list)
        for i in range(len(thread_num_index_dict)):
            res_str = ''
            for j in range(len(model_parallel_index_dict)):
                index = i * len(model_parallel_index_dict) + j
                if j == len(model_parallel_index_dict) - 1:
                    if res_list[index] == None:
                        res_str += '\n'
                    else:
                        res_str += str(res_list[index]) + '\n'
                else:
                    if res_list[index] == None:
                        res_str += ','
                    else:
                        res_str += str(res_list[index]) + ','
            print(res_str)
            file_writer.write(res_str)

    finally:
        if file_reader:
            file_reader.close()
            file_writer.close()
if __name__ == '__main__':
    ssd_mobilenetv1_sparse_fp16_best_config_list = [1, 4, 1, 8]
    get_bs_vs_tn('ssd_mobilenetv1-sparse-fp16.txt', 'bs_tn.txt', ssd_mobilenetv1_sparse_fp16_best_config_list)
    get_bs_vs_dp('ssd_mobilenetv1-sparse-fp16.txt', 'bs_dp.txt', ssd_mobilenetv1_sparse_fp16_best_config_list)
    get_bs_vs_mp('ssd_mobilenetv1-sparse-fp16.txt', 'bs_mp.txt', ssd_mobilenetv1_sparse_fp16_best_config_list)
    #get_tn_vs_dp('ssd_mobilenetv1-sparse-fp16.txt', 'tn_dp.txt', ssd_mobilenetv1_sparse_fp16_best_config_list)
    #get_tn_vs_mp('ssd_mobilenetv1-sparse-fp16.txt', 'tn_mp.txt', ssd_mobilenetv1_sparse_fp16_best_config_list)
    get_dp_vs_mp('ssd_mobilenetv1-sparse-fp16.txt', 'dp_mp.txt', ssd_mobilenetv1_sparse_fp16_best_config_list)

