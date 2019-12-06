# coding=utf-8
#!/usr/bin/env python3

import os


if __name__ == '__main__':
    '''
    This script tries to find the first crashed point log file. Steps:
      1. Simulate the offline model generator, get the offline model file list;
      2. Simulate the enumeration based runner, get the output log file list;
      3. Scan the failed log directory, get the failed log file list;
      4. Scan the output log file list, and the failed log file list, find out
         the first crashed point log file.
    '''
    # [1, 2, 4, 8, 16, 32, 64]
    batch_size_list = [2**i for i in range(7)]
    thread_num_list = [2**i for i in range(7)]
    # [(1, 1), (1, 2), (1, 4), ..., (1, 32), (2, 1), ..., (2, 16), ..., (32, 1)]
    dp_mp_list = [(2**i, 2**j) for i in range(6)
                                   for j in range(6)
                                       if 2**i * 2**j <= 32]
    # Note we need to gurantte the shell execution order, better to hard code the dp_mp_list
    dp_mp_list = [
    (1, 1), (1, 2),
    (1, 4), (1, 8),
    (2, 1), (2, 2),
    (2, 4), (2, 8),
    (4, 1), (4, 2),
    (4, 4), (4, 8),
    (8, 1), (8, 2),
    (8, 4),
    (1, 16), (1, 32), (2, 16),
    (16, 1), (16, 2), (32, 1)]

    print(len(dp_mp_list))
    print(dp_mp_list)
    # [1, 2, 3, 4, 5]
    round_list = [i for i in range(1, 6)]
    # [1, 2, 4, 8, 16, 32]
    mp_list = [2**i for i in range(6)]
    NN_NAME = 'ssd_mobilenetv1'
    NN_PATH_PREFIX = '../offline-' + NN_NAME
    offline_model_list = []
    for batch in batch_size_list:
        for mp in mp_list:
            offline_model_name = 'offline-' + NN_NAME + '-dense-fp16-' + str(batch) + 'batch-' + str(mp) + '.cambricon'
            dir_name = NN_PATH_PREFIX + '/'
            # Note: Sometimes, we may fail to generate the offline models.
            # This step is necessary.
            if os.path.exists(dir_name + offline_model_name):
                offline_model_list.append(offline_model_name)
    #print(offline_model_list)

    # get the real failed file list, we use the 'log' keyword to ignore the python or bash scripts
    real_failed_log_file_list = {str(f) for f in os.listdir('.') if os.path.isfile(f) and 'log' in str(f)}
    print(len(real_failed_log_file_list))
    # get the crashed point file
    log_file_list = []
    for counter in round_list:
        for batch in batch_size_list:
            for thread_num in thread_num_list:
                for dpmp in dp_mp_list:
                    dp , mp = dpmp[0], dpmp[1]
                    offline_model_name = 'offline-' + NN_NAME + '-dense-fp16-' + str(batch) + 'batch-' + str(mp) + '.cambricon'
                    dir_name = NN_PATH_PREFIX + '/'
                    # Only if the offline model file exists, we can generate the log file
                    if os.path.exists(dir_name + offline_model_name):
                        log_file_list.append(NN_NAME + '.log-fp16-dense-' + str(batch) + 'batch-' + str(dp) + '-' + str(mp) + '-' + str(thread_num) + '-round-' + str(counter))
    #print(log_file_list)

    for i, file in enumerate(log_file_list):
        if log_file_list[i] in real_failed_log_file_list and   \
           log_file_list[i+1] in real_failed_log_file_list and \
           log_file_list[i+2] in real_failed_log_file_list and \
           log_file_list[i+3] in real_failed_log_file_list and \
           log_file_list[i+4] in real_failed_log_file_list and \
           log_file_list[i+5] in real_failed_log_file_list and \
           log_file_list[i+6] in real_failed_log_file_list and \
           log_file_list[i+7] in real_failed_log_file_list and \
           log_file_list[i+8] in real_failed_log_file_list and \
           log_file_list[i+9] in real_failed_log_file_list:
            # find the first crashed point log file
            print(log_file_list[i])
            exit(0)
    print('Whooooops, fail to find the crashed point file!')

