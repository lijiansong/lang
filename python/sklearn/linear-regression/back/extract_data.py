#!/usr/bin/env python3

import sys
import re
import os
import collections

def extract_end2end_fps(end2end_file_path):
    file_reader = open(end2end_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-end2end_fps.txt', 'w')
    data_list = []
    sparse_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            end2end_fps = float(line_str[3])
            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            sparse_round_count[sparsity_num] = sparse_round_count.get(sparsity_num, 0) + 1
            batch_size = re.findall(r'\d+', batch_size)
            data_list.append([sparsity_num, batch_size[0], data_parallel, model_parallel, thread_num, end2end_fps, round_num])
        print(data_list)
        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[1], x[2], x[3], x[4]))
        res_dict = {}
        for line in data_list:
            sparsity_num, batch_size, data_parallel, model_parallel, thread_num, end2end_fps, round_num = line[0], line[1], line[2], line[3], line[4], line[5], line[6]
            res_dict[sparsity_num] = res_dict.get(sparsity_num, 0) + end2end_fps/sparse_round_count[sparsity_num]
        print(res_dict)
        print(sparse_round_count)
        od = collections.OrderedDict(sorted(res_dict.items()))
        # write to file
        for k, v in od.items():
            res = str(k) + ',' + str(v) + '\n'
            file_writer.write(res)

    finally:
        file_reader.close()
        file_writer.close()

def extract_hardware_fps(hw_fps_file_path):
    file_reader = open(hw_fps_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-hardware_fps.txt', 'w')
    data_list = []
    sparse_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            end2end_fps = float(line_str[3])
            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            sparse_round_count[sparsity_num] = sparse_round_count.get(sparsity_num, 0) + 1
            batch_size = re.findall(r'\d+', batch_size)
            data_list.append([sparsity_num, batch_size[0], data_parallel, model_parallel, thread_num, end2end_fps, round_num])

        print(data_list)
        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[1], x[2], x[3], x[4]))
        res_dict = {}
        for line in data_list:
            sparsity_num, batch_size, data_parallel, model_parallel, thread_num, end2end_fps, round_num = line[0], line[1], line[2], line[3], line[4], line[5], line[6]
            res_dict[sparsity_num] = res_dict.get(sparsity_num, 0) + end2end_fps/sparse_round_count[sparsity_num]
        print(res_dict)
        print(sparse_round_count)
        od = collections.OrderedDict(sorted(res_dict.items()))
        # write to file
        for k, v in od.items():
            res = str(k) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_total_exe_time(exe_time_file_path):
    file_reader = open(exe_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-total-exe-time.txt', 'w')
    data_list = []
    sparse_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            exe_time = line_str[3]
            print(exe_time)
            # exe_time will be like this:
            # 1.23677e+06 us
            exe_time, _ = exe_time.split()
            print(exe_time)

            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            sparse_round_count[sparsity_num] = sparse_round_count.get(sparsity_num, 0) + 1
            batch_size = re.findall(r'\d+', batch_size)
            data_list.append([sparsity_num, batch_size[0], data_parallel, model_parallel, thread_num, int(float(exe_time)), round_num])

        print(data_list)
        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[1], x[2], x[3], x[4]))
        res_dict = {}
        for line in data_list:
            sparsity_num, batch_size, data_parallel, model_parallel, thread_num, total_exe_time, round_num = line[0], line[1], line[2], line[3], line[4], line[5], line[6]
            res_dict[sparsity_num] = res_dict.get(sparsity_num, 0) + total_exe_time/sparse_round_count[sparsity_num]
        print(res_dict)
        print(sparse_round_count)
        od = collections.OrderedDict(sorted(res_dict.items()))
        # write to file
        for k, v in od.items():
            res = str(k) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit("Usage: must 4 args!")
    end2end_file = sys.argv[1]
    hw_fps_file = sys.argv[2]
    time_log_file = sys.argv[3]
    extract_end2end_fps(end2end_file)
    extract_hardware_fps(hw_fps_file)
    extract_total_exe_time(time_log_file)
