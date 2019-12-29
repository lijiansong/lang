#!/usr/bin/env python3

import sys
import re
import os
import collections

def extract_global_acc(acc_file_path):
    file_reader = open(acc_file_path, 'r')
    prefix = os.getcwd().split("/")[-1]
    file_writer = open(prefix + '-global-acc.txt', 'w')
    data_list = []
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 1)
            #print(line_str)
            line_no = int(line_str[1])
            file_name = line_str[0]
            _, _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)
            batch_size = re.findall(r'\d+', batch_size)
            # shell cmd: sed -n $(line_no + 1)p file_name
            cmd = 'sed -n ' + str(line_no + 1) + 'p ' + file_name
            shell_exe_res = os.popen(cmd).read()
            #print(shell_exe_res)
            # shell_exe_res will be like this:
            # accuracy1: 0.8439 (8439/10000)
            global_acc1 = shell_exe_res.split(" ", 2)[1]
            data_list.append([int(batch_size[0]), int(data_parallel), int(model_parallel), int(thread_num), float(global_acc1), round_num])
        #print(data_list)
        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[0], x[1], x[2], x[3]))
        res_dict = {}
        case_num_count = {}
        for line in data_list:
            batch_size, data_parallel, model_parallel, thread_num, global_acc1, round_num = line[0], line[1], line[2], line[3], line[4], line[5]
            if (batch_size, data_parallel, model_parallel, thread_num) in case_num_count:
                case_num_count[(batch_size, data_parallel, model_parallel, thread_num)] += 1
            else:
                case_num_count[(batch_size, data_parallel, model_parallel, thread_num)] = 1
            if (batch_size, data_parallel, model_parallel, thread_num) in res_dict:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] += float(global_acc1)
            else:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] = float(global_acc1)
        print(res_dict)
        print(case_num_count)
        od = collections.OrderedDict(sorted(res_dict.items(), key = lambda x: (x[0][0], x[0][1], x[0][2], x[0][3])))
        #res_list = []
        # write to file
        for k, v in od.items():
            #res_list.append([k[0], k[1], k[2], k[3], v / case_num_count[k]])
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ','+ str(v / case_num_count[k]) + '\n'
            file_writer.write(res)

        #res_list = sorted(res_list, key = lambda x: (x[0], x[1], x[2], x[3]))
        #for i in res_list:
        #    res = str(i[0]) + ',' + str(i[1]) + ',' + str(i[2]) + ',' + str(i[3]) + ',' + str(i[4]) + '\n'
        #    file_writer.write(res)

    finally:
        file_reader.close()
        file_writer.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: must 2 args!")
    acc_file = sys.argv[1]
    extract_global_acc(acc_file)
