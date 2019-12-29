#!/usr/bin/env python3

import sys
import re
import os
import collections

def extract_global_acc(acc_file_path):
    file_reader = open(acc_file_path, 'r')
    prefix = os.getcwd().split("/")[-1]
    file_writer = open(prefix + '-global-acc.txt', 'w')
    res_dict = {}
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
            _, _, _, sparsity, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity = float(sparsity)
            round_num = int(round_num)
            batch_size = re.findall(r'\d+', batch_size)
            # shell cmd: sed -n $(line_no + 1)p file_name
            cmd = 'sed -n ' + str(line_no + 1) + 'p ' + file_name
            shell_exe_res = os.popen(cmd).read()
            #print(shell_exe_res)
            # shell_exe_res will be like this:
            # accuracy1: 0.8439 (8439/10000)
            global_acc1 = shell_exe_res.split(" ", 2)[1]
            # Notice: For each round, top-1 acc must be the same!
            res_dict[sparsity] = global_acc1
        print(res_dict)
        # sort data_list by multiple keys
        od = collections.OrderedDict(sorted(res_dict.items()))
        # write to file
        for k, v in od.items():
            res = str(k) + ',' + str(v) + '\n'
            file_writer.write(res)

    finally:
        file_reader.close()
        file_writer.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit("Usage: must 2 args!")
    acc_file = sys.argv[1]
    extract_global_acc(acc_file)
