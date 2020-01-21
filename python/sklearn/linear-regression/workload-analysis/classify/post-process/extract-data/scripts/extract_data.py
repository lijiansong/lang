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
    case_round_count = {}
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
            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)

            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)] += 1
            else:
                case_round_count[(bs, dp, mp, thread_num)] = 1
            data_list.append([bs, dp, mp, thread_num, end2end_fps, round_num])
        #print(data_list)
        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[0], x[1], x[2], x[3]))
        res_dict = {}
        for line in data_list:
            batch_size, data_parallel, model_parallel, thread_num, end2end_fps, round_num = line[0], line[1], line[2], line[3], line[4], line[5]
            if (batch_size, data_parallel, model_parallel, thread_num) in res_dict:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] += end2end_fps/case_round_count[(batch_size, data_parallel, model_parallel, thread_num)]
            else:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] = end2end_fps/case_round_count[(batch_size, data_parallel, model_parallel, thread_num)]
        print(res_dict)
        print(case_round_count)
        od = collections.OrderedDict(sorted(res_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, end2end fps
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_hardware_fps(hw_fps_file_path):
    file_reader = open(hw_fps_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-hardware_fps.txt', 'w')
    data_list = []
    case_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            hw_fps = float(line_str[3])
            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)
            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)] += 1
            else:
                case_round_count[(bs, dp, mp, thread_num)] = 1
            data_list.append([bs, dp, mp, thread_num, hw_fps, round_num])

        #print(data_list)
        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[1], x[2], x[3], x[4]))
        res_dict = {}
        for line in data_list:
            batch_size, data_parallel, model_parallel, thread_num, hw_fps, round_num = line[0], line[1], line[2], line[3], line[4], line[5]
            if (batch_size, data_parallel, model_parallel, thread_num) in res_dict:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] += hw_fps/case_round_count[(batch_size, data_parallel, model_parallel, thread_num)]
            else:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] = hw_fps/case_round_count[(batch_size, data_parallel, model_parallel, thread_num)]

        print(res_dict)
        print(case_round_count)
        od = collections.OrderedDict(sorted(res_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, hw fps
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_total_exe_time(exe_time_file_path):
    file_reader = open(exe_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-total-exe-time.txt', 'w')
    data_list = []
    case_round_count = {}
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
            #print(exe_time)
            # exe_time will be like this:
            # 1.23677e+06 us
            exe_time, _ = exe_time.split()
            #print(exe_time)

            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)
            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            exe_time = int(float(exe_time))
            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)] += 1
            else:
                case_round_count[(bs, dp, mp, thread_num)] = 1
            data_list.append([bs, dp, mp, thread_num, exe_time, round_num])

        # sort data_list by multiple keys
        data_list = sorted(data_list, key = lambda x: (x[1], x[2], x[3], x[4]))
        res_dict = {}
        for line in data_list:
            batch_size, data_parallel, model_parallel, thread_num, total_exe_time, round_num = line[0], line[1], line[2], line[3], line[4], line[5]
            if (batch_size, data_parallel, model_parallel, thread_num) in res_dict:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] += total_exe_time/case_round_count[(batch_size, data_parallel, model_parallel, thread_num)]
            else:
                res_dict[(batch_size, data_parallel, model_parallel, thread_num)] = total_exe_time/case_round_count[(batch_size, data_parallel, model_parallel, thread_num)]
        print(res_dict)
        print(case_round_count)
        od = collections.OrderedDict(sorted(res_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, total execution time
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_prepare_input(prepare_input_file_path):
    file_reader = open(prepare_input_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-prepare_input.txt', 'w')
    data_record_dict = {}
    case_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            # convert from u-second into micro-second
            prepare_input_time = float(line_str[3].split()[0])
            prepare_input_time /= 1000
            #print(prepare_input_time)
            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)

            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            if (bs, dp, mp, thread_num) in data_record_dict:
                data_record_dict[(bs, dp, mp, thread_num)] += prepare_input_time
            else:
                data_record_dict[(bs, dp, mp, thread_num)] = prepare_input_time

            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)].add(round_num)
            else:
                case_round_count[(bs, dp, mp, thread_num)] = set({round_num})

        print(case_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(case_round_count[k])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, prepare input time
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_copyin_time(copyin_time_file_path):
    file_reader = open(copyin_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-copyin_time.txt', 'w')
    data_record_dict = {}
    case_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            # convert from u-second into micro-second
            copyin_time = float(line_str[3].split()[0])
            copyin_time /= 1000
            #print(copyin_time)
            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)

            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            if (bs, dp, mp, thread_num) in data_record_dict:
                data_record_dict[(bs, dp, mp, thread_num)] += copyin_time
            else:
                data_record_dict[(bs, dp, mp, thread_num)] = copyin_time

            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)].add(round_num)
            else:
                case_round_count[(bs, dp, mp, thread_num)] = set({round_num})

        print(case_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(case_round_count[k])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, copyin time
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_execution_time(execution_time_file_path):
    file_reader = open(execution_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-execution_time.txt', 'w')
    data_record_dict = {}
    case_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            # convert from u-second into micro-second
            execution_time = float(line_str[3].split()[0])
            execution_time /= 1000
            #print(execution_time)
            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)

            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            if (bs, dp, mp, thread_num) in data_record_dict:
                data_record_dict[(bs, dp, mp, thread_num)] += execution_time
            else:
                data_record_dict[(bs, dp, mp, thread_num)] = execution_time

            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)].add(round_num)
            else:
                case_round_count[(bs, dp, mp, thread_num)] = set({round_num})

        print(case_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(case_round_count[k])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, execution time
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_copyout_time(copyout_time_file_path):
    file_reader = open(copyout_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-copyout_time.txt', 'w')
    data_record_dict = {}
    case_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            # convert from u-second into micro-second
            copyout_time = float(line_str[3].split()[0])
            copyout_time /= 1000
            #print(copyout_time)
            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)

            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            if (bs, dp, mp, thread_num) in data_record_dict:
                data_record_dict[(bs, dp, mp, thread_num)] += copyout_time
            else:
                data_record_dict[(bs, dp, mp, thread_num)] = copyout_time

            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)].add(round_num)
            else:
                case_round_count[(bs, dp, mp, thread_num)] = set({round_num})

        print(case_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(case_round_count[k])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, copyout time
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_post_process_time(post_process_time_file_path):
    file_reader = open(post_process_time_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-post_process_time.txt', 'w')
    data_record_dict = {}
    case_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            #print(line_str)
            # convert from u-second into micro-second
            post_process_time = float(line_str[3].split()[0])
            post_process_time /= 1000
            #print(post_process_time)
            _, _, _, batch_size, data_parallel, model_parallel, thread_num, _, round_num = line_str[0].split("-")
            round_num = int(round_num)

            batch_size = re.findall(r'\d+', batch_size)
            bs = int(batch_size[0])
            dp = int(data_parallel)
            mp = int(model_parallel)
            thread_num = int(thread_num)
            if (bs, dp, mp, thread_num) in data_record_dict:
                data_record_dict[(bs, dp, mp, thread_num)] += post_process_time
            else:
                data_record_dict[(bs, dp, mp, thread_num)] = post_process_time

            if (bs, dp, mp, thread_num) in case_round_count:
                case_round_count[(bs, dp, mp, thread_num)].add(round_num)
            else:
                case_round_count[(bs, dp, mp, thread_num)] = set({round_num})

        print(case_round_count)
        for k, v in data_record_dict.items():
            data_record_dict[k] = v / len(case_round_count[k])
        od = collections.OrderedDict(sorted(data_record_dict.items(), key = lambda x : (x[0][0], x[0][1], x[0][2], x[0][3])))
        # write to file
        for k, v in od.items():
            # batch size, data parallel, model parallel, thread num, post process time
            res = str(k[0]) + ',' + str(k[1]) + ',' + str(k[2]) + ',' + str(k[3]) + ',' + str(v) + '\n'
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()
if __name__ == '__main__':
    if len(sys.argv) < 9:
        sys.exit("Usage: must 9 args!")
    end2end_file = sys.argv[1]
    hw_fps_file = sys.argv[2]
    time_log_file = sys.argv[3]
    prepare_input_time_file = sys.argv[4]
    copyin_time_file = sys.argv[5]
    execution_time_file = sys.argv[6]
    copyout_time_file = sys.argv[7]
    post_process_time_file = sys.argv[8]
    extract_end2end_fps(end2end_file)
    extract_hardware_fps(hw_fps_file)
    extract_total_exe_time(time_log_file)
    extract_prepare_input(prepare_input_time_file)
    extract_copyin_time(copyin_time_file)
    extract_execution_time(execution_time_file)
    extract_copyout_time(copyout_time_file)
    extract_post_process_time(post_process_time_file)
