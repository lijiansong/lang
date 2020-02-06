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

def extract_prepare_input(prepare_input_file_path):
    file_reader = open(prepare_input_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-prepare_input.txt', 'w')
    data_record_dict = {}
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
            # prepare_input_time will be like this:
            # 1919 us
            # convert it into micro-second
            prepare_input_time = float(line_str[3].split()[0])/1000
            #print(prepare_input_time)

            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            bs = int(re.findall(r'\d+', batch_size)[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            tn = int(thread_num)
            if (sparsity_num, bs, dp, mp, tn) in data_record_dict:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] += prepare_input_time
            else:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] = prepare_input_time

            if sparsity_num in sparse_round_count:
                sparse_round_count[sparsity_num].add(round_num)
            else:
                sparse_round_count[sparsity_num] = set({round_num})
        print(sparse_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(sparse_round_count[k[0]])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4])))
        # write to file
        for k, v in od.items():
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(k[4]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_copyin_time(copyin_time_file_path):
    file_reader = open(copyin_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-copyin_time.txt', 'w')
    data_record_dict = {}
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
            # convert it into micro-second
            copyin_time = float(line_str[3].split()[0])/1000

            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            bs = int(re.findall(r'\d+', batch_size)[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            tn = int(thread_num)
            if (sparsity_num, bs, dp, mp, tn) in data_record_dict:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] += copyin_time
            else:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] = copyin_time

            if sparsity_num in sparse_round_count:
                sparse_round_count[sparsity_num].add(round_num)
            else:
                sparse_round_count[sparsity_num] = set({round_num})
        print(sparse_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(sparse_round_count[k[0]])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4])))
        # write to file
        for k, v in od.items():
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(k[4]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_execution_time(execution_time_file_path):
    file_reader = open(execution_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-execution_time.txt', 'w')
    data_record_dict = {}
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
            # convert it into micro-second
            execution_time = float(line_str[3].split()[0])/1000

            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            bs = int(re.findall(r'\d+', batch_size)[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            tn = int(thread_num)
            if (sparsity_num, bs, dp, mp, tn) in data_record_dict:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] += execution_time
            else:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] = execution_time

            if sparsity_num in sparse_round_count:
                sparse_round_count[sparsity_num].add(round_num)
            else:
                sparse_round_count[sparsity_num] = set({round_num})
        print(sparse_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(sparse_round_count[k[0]])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4])))
        # write to file
        for k, v in od.items():
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(k[4]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_copyout_time(copyout_time_file_path):
    file_reader = open(copyout_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-copyout_time.txt', 'w')
    data_record_dict = {}
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
            # convert it into micro-second
            copyout_time = float(line_str[3].split()[0])/1000

            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            bs = int(re.findall(r'\d+', batch_size)[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            tn = int(thread_num)
            if (sparsity_num, bs, dp, mp, tn) in data_record_dict:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] += copyout_time
            else:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] = copyout_time

            if sparsity_num in sparse_round_count:
                sparse_round_count[sparsity_num].add(round_num)
            else:
                sparse_round_count[sparsity_num] = set({round_num})
        print(sparse_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(sparse_round_count[k[0]])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4])))
        # write to file
        for k, v in od.items():
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(k[4]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_post_process_time(post_process_time_file_path):
    file_reader = open(post_process_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-post_process_time.txt', 'w')
    data_record_dict = {}
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
            # convert it into micro-second
            post_process_time = float(line_str[3].split()[0])/1000

            _, _, _, sparsity_num, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            sparsity_num = float(sparsity_num)
            round_num = int(round_num)
            bs = int(re.findall(r'\d+', batch_size)[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            tn = int(thread_num)
            if (sparsity_num, bs, dp, mp, tn) in data_record_dict:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] += post_process_time
            else:
                data_record_dict[(sparsity_num, bs, dp, mp, tn)] = post_process_time

            if sparsity_num in sparse_round_count:
                sparse_round_count[sparsity_num].add(round_num)
            else:
                sparse_round_count[sparsity_num] = set({round_num})
        print(sparse_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(sparse_round_count[k[0]])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3], x[0][4])))
        # write to file
        for k, v in od.items():
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(k[4]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

if __name__ == '__main__':
    if len(sys.argv) < 10:
        sys.exit("Usage: must 10 args!")
    end2end_file = sys.argv[1]
    hw_fps_file = sys.argv[2]
    time_log_file = sys.argv[3]
    acc_log_file = sys.argv[4]
    prepare_input_time_file = sys.argv[5]
    copyin_time_file = sys.argv[6]
    execution_time_file = sys.argv[7]
    copyout_time_file = sys.argv[8]
    post_process_time_file = sys.argv[9]
    extract_end2end_fps(end2end_file)
    extract_hardware_fps(hw_fps_file)
    extract_total_exe_time(time_log_file)
    extract_final_acc(acc_log_file)
    extract_prepare_input(prepare_input_time_file)
    extract_copyin_time(copyin_time_file)
    extract_execution_time(execution_time_file)
    extract_copyout_time(copyout_time_file)
    extract_post_process_time(post_process_time_file)
