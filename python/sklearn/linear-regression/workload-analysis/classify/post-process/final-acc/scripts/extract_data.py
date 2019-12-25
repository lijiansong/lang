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
    # best config list: batch size, data parallelism, model parallelism, thread number
    best_config_batch_size = best_config_data_parallel = best_config_model_parallel = best_config_thread_num = 0
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
            batch_size = re.findall(r'\d+', batch_size)[0]
            data_parallel = int(data_parallel)
            model_parallel = int(model_parallel)
            thread_num = int(thread_num)
            best_config_batch_size, best_config_data_parallel, best_config_model_parallel, best_config_thread_num = \
                    batch_size, data_parallel, model_parallel, thread_num
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
            res = str(k) + ',' + str(best_config_batch_size) + ',' + str(best_config_data_parallel) + ',' + str(best_config_model_parallel) + ',' + str(best_config_thread_num) + ',' + str(v) + '\n'
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

def extract_final_acc(acc_file_path):
    file_reader = open(acc_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-final_acc.txt', 'w')
    data_list = []
    sparse_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 1)
            #print(line_str)
            final_acc = float(line_str[1])
            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            sparse_round_count[sparsity_num] = sparse_round_count.get(sparsity_num, 0) + 1
            batch_size = re.findall(r'\d+', batch_size)
            data_list.append([sparsity_num, batch_size[0], data_parallel, model_parallel, thread_num, final_acc, round_num])
        print(data_list)
        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[1], x[2], x[3], x[4]))
        res_dict = {}
        for line in data_list:
            sparsity_num, batch_size, data_parallel, model_parallel, thread_num, final_acc, round_num = line[0], line[1], line[2], line[3], line[4], line[5], line[6]
            res_dict[sparsity_num] = res_dict.get(sparsity_num, 0) + final_acc/sparse_round_count[sparsity_num]
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

def extract_io_time(in_time_file_path, io_suffix):
    file_reader = open(in_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + io_suffix, 'w')
    sparse_round_count = {}
    res_dict = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":")
            #print(line_str)
            io_time = line_str[3]
            #print(io_time)
            # exe_time will be like this:
            # 385 us
            io_time, _ = io_time.split()
            #print(io_time)
            io_time = float(io_time)
            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            # Note: sparse_round_count is a dict, whose key is 'sparsity_num', value is a set of 'round_num'.
            if sparsity_num in sparse_round_count:
                sparse_round_count[sparsity_num].add(round_num)
            else:
                sparse_round_count[sparsity_num]=set()
                sparse_round_count[sparsity_num].add(round_num)
            batch_size = re.findall(r'\d+', batch_size)

            res_dict[sparsity_num] = res_dict.get(sparsity_num, 0) + io_time

        print(res_dict)
        print(sparse_round_count)
        od = collections.OrderedDict(sorted(res_dict.items()))
        # write to file
        for k, v in od.items():
            res = str(k) + ',' + str(v/len(sparse_round_count[k])) + '\n'
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
