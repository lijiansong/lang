#!/usr/bin/env python3

import os
import sys
import collections
import pickle

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

def calculate_in_gb(dram_throughput_):
    '''
    Note: dram_read_throughput and dram_write_throughput is in GB/s,
    the value can be 17.113GB/s or 17.113MB/s or 17.113B/s
    '''
    # 17.113G or 17.113M or 17.113K or 17.113
    dram_throughput = dram_throughput_.split('B')[0]
    if 'G' in dram_throughput:
        dram_throughput = float(dram_throughput.split('G')[0])
    elif 'M' in dram_throughput:
        dram_throughput = float(dram_throughput.split('M')[0]) / 1e3
    elif 'K' in dram_throughput:
        dram_throughput = float(dram_throughput.split('K')[0]) / 1e6
    else:
        dram_throughput = float(dram_throughput) / 1e9
    return dram_throughput


def extract_flops_membwd(profiling_log_file, mem_transactions_log_file, debug=True):
    nvprof_log_reader = open(profiling_log_file, 'r')
    mem_transactions_log_reader = open(mem_transactions_log_file, 'r')
    nvprof_log_writer = open('nvprof-log.txt', 'wb')
    mem_transactions_writer = open('nvprof-mem-transactions.txt', 'wb')
    kernel_names_writer = open('nvprof-kernel-names.txt', 'wb')
    # key is kernel name, value is a tuple: <Invocations, flop_count_sp, dram_read_throughput, dram_write_throughput>
    flops_membwd_record_dict = {}
    mem_transactions_record_dict = {}
    kernel_names_set = set()
    try:
        lines_list = nvprof_log_reader.readlines()
        # line will be like this:
        # Invocations   Metric Name     Metric Description   Min     Max     Avg
        for i, line in enumerate(lines_list):
            line = line.rstrip('\n')
            if 'Kernel:' in line:
                # 1. extract the kernel name
                #kernel_name = ''
                #for item in line.split()[1:]:
                #    kernel_name += item
                kernel_name = line.replace('Kernel: ', '')
                kernel_name = kernel_name.strip()
                kernel_name = kernel_name.replace('*', '\*')
                kernel_names_set.add(kernel_name)
                # 2. next three lines will be flop_count_sp, dram_read_throughput
                # and dram_write_throughput
                invocations = int(lines_list[i+1].split()[0])
                flop_count_sp = int(lines_list[i+1].split()[-1])
                # Note: dram_read_throughput and dram_write_throughput is in GB/s,
                # the value can be 17.113GB/s or 17.113MB/s or 17.113B/s
                dram_read_throughput = lines_list[i+2].split()[-1]
                # 17.113G or 17.113M or 17.113K or 17.113
                dram_read_throughput = calculate_in_gb(dram_read_throughput)
                dram_write_throughput = lines_list[i+3].split()[-1]
                dram_write_throughput = calculate_in_gb(dram_write_throughput)
                if debug:
                    print(kernel_name)
                    print(dram_read_throughput, 'GB/s')
                    print(dram_write_throughput, 'GB/s')
                flops_membwd_record_dict[kernel_name] = (invocations, flop_count_sp, dram_read_throughput, dram_write_throughput)
            else:
                continue

        # extract dram_read_transactions and dram_write_transactions
        mem_transactions_lines_list = mem_transactions_log_reader.readlines()
        # line will be like this:
        # Invocations   Metric Name     Metric Description   Min     Max     Avg
        for i, line in enumerate(mem_transactions_lines_list):
            if 'Kernel:' in line:
                # 1. extract the kernel name
                #kernel_name = ''
                #for item in line.split()[1:]:
                #    kernel_name += item
                kernel_name = line.replace('Kernel: ', '')
                kernel_name = kernel_name.strip()
                kernel_name = kernel_name.replace('*', '\*')
                # 2. next two lines will be dram_read_transactions and dram_write_transactions
                invocations = int(mem_transactions_lines_list[i+1].split()[0])
                dram_read_transactions = float(mem_transactions_lines_list[i+1].split()[-1])
                dram_write_transactions = float(mem_transactions_lines_list[i+2].split()[-1])
                mem_transactions_record_dict[kernel_name] = (invocations, dram_read_transactions, dram_write_transactions)
            else:
                continue
        if debug:
            print(flops_membwd_record_dict)
            print(mem_transactions_record_dict)
            print(kernel_names_set)
        pickle.dump(flops_membwd_record_dict, nvprof_log_writer)
        pickle.dump(mem_transactions_record_dict, mem_transactions_writer)
        pickle.dump(kernel_names_set, kernel_names_writer)
    finally:
        nvprof_log_reader.close()
        mem_transactions_log_reader.close()
        nvprof_log_writer.close()
        mem_transactions_writer.close()
        kernel_names_writer.close()


def cvt_to_micro_second(time_str):
    # time str can be: 4.9920ms, 4.9920us or 4.9920ns
    # convert into micro second
    time_val = time_str.split('s')[0]
    if time_val[-1] == 'm':
        return float(time_val.split('m')[0])
    elif time_val[-1] == 'u':
        return float(time_val.split('u')[0])/1e3
    elif time_val[-1] == 'n':
        return float(time_val.split('n')[0])/1e6

def excel_io(net_name, batch_size, gpu_trace_log_file, debug=True):
    nvprof_flops_membwd_reader = open('nvprof-log.txt', 'rb')
    nvprof_mem_transactions_reader = open('nvprof-mem-transactions.txt', 'rb')
    kernel_names_reader = open('nvprof-kernel-names.txt', 'rb')
    flops_membwd_record_dict = pickle.load(nvprof_flops_membwd_reader)
    mem_transactions_record_dict = pickle.load(nvprof_mem_transactions_reader)
    kernel_names_set = pickle.load(kernel_names_reader)

    if debug:
        print(flops_membwd_record_dict)
        print(mem_transactions_record_dict)
        print(kernel_names_set)

    # execution time of each kernel
    kernel_exe_time_dict = {}
    for kernel_name in kernel_names_set:
        cmd = 'grep -rin \"' + str(kernel_name) + '\" ' + str(gpu_trace_log_file)
        #print(cmd)
        shell_exe_res = os.popen(cmd).readlines()
        #print(shell_exe_res)
        for item in shell_exe_res:
            kernel_exe_time_dict[kernel_name] = kernel_exe_time_dict.get(kernel_name, 0) + cvt_to_micro_second(item.split()[1])
            #print(item)
    print(kernel_exe_time_dict)

    # total kernel execution time
    all_kernels_execution_time = 0
    for k, v in kernel_exe_time_dict.items():
        all_kernels_execution_time += float(v)
    print(all_kernels_execution_time)

    kernel_list = []
    invocations_list = []
    flop_count_sp_list = []
    dram_read_throughput_list = []
    dram_write_throughput_list = []
    kernel_exe_time_list = []
    kernel_exe_time_ratio_list = []

    mem_transactions_kernel_list = []
    mem_transactions_invocations_list = []
    dram_read_transactions_list = []
    dram_write_transactions_list = []

    try:
        for k, v in flops_membwd_record_dict.items():
            kernel_list.append(k)
            invocations_list.append(int(v[0]))
            flop_count_sp_list.append(int(v[1]))
            dram_read_throughput_list.append(float(v[2]))
            dram_write_throughput_list.append(float(v[3]))
            kernel_exe_time_list.append(float(kernel_exe_time_dict[k]))
            kernel_exe_time_ratio_list.append(float(kernel_exe_time_dict[k]) / all_kernels_execution_time * 100.0)

        for k, v in mem_transactions_record_dict.items():
            mem_transactions_kernel_list.append(k)
            mem_transactions_invocations_list.append(int(v[0]))
            dram_read_transactions_list.append(float(v[1]))
            dram_write_transactions_list.append(float(v[2]))

    finally:
        nvprof_flops_membwd_reader.close()
        nvprof_mem_transactions_reader.close()

    assert len(kernel_list) == len(invocations_list) and \
            len(invocations_list) == len(flop_count_sp_list) and \
            len(flop_count_sp_list) == len(dram_read_throughput_list) and \
            len(dram_read_throughput_list) == len(dram_write_throughput_list) and \
            len(mem_transactions_kernel_list) == len(mem_transactions_invocations_list) and \
            len(mem_transactions_invocations_list) == len(dram_read_transactions_list) and \
            len(dram_read_transactions_list) == len(dram_write_transactions_list), \
            " Error! Must have same records length!"

    # calculate the total flop_count_sp and average dram_read_throughput, dram_write_throughput
    # note that the average dram_write_throughput and dram_read_throughput is calculated by their
    # execution time ratio.
    total_invocations = 0
    for item in invocations_list:
        total_invocations += item
    total_flop_count_sp = 0
    avg_dram_read_throughput = 0
    avg_dram_write_throughput = 0
    for i, invos in enumerate(invocations_list):
        total_flop_count_sp += flop_count_sp_list[i] * invos
        avg_dram_read_throughput += (dram_read_throughput_list[i] * kernel_exe_time_ratio_list[i] / 100.0)
        avg_dram_write_throughput += (dram_write_throughput_list[i] * kernel_exe_time_ratio_list[i] / 100.0)

    # calculate the total dram_read_transactions, dram_write_transactions
    total_invocations = 0
    total_dram_read_transactions = 0
    total_dram_write_transactions = 0
    for item in mem_transactions_invocations_list:
        total_invocations += item
    for i, invos in enumerate(mem_transactions_invocations_list):
        total_dram_read_transactions += (dram_read_transactions_list[i] * invos)
        total_dram_write_transactions += (dram_write_transactions_list[i] * invos)

    value_list = [total_flop_count_sp, avg_dram_read_throughput, avg_dram_write_throughput, total_dram_read_transactions, total_dram_write_transactions, all_kernels_execution_time]
    name_list = ['total_flop_count_sp', 'avg_dram_read_throughput', 'avg_dram_write_throughput', 'total_dram_read_transactions', 'total_dram_write_transactions', 'all_kernels exe_time']


    sheet1_od = collections.OrderedDict()
    sheet1_od['kernel name'] = kernel_list
    sheet1_od['invocations'] = invocations_list
    sheet1_od['flop_count_sp'] = flop_count_sp_list
    sheet1_od['dram_read_throughput(GB/s)'] = dram_read_throughput_list
    sheet1_od['dram_write_throughput_list(GB/s)'] = dram_write_throughput_list
    sheet1_od['kernel execution time(ms)'] = kernel_exe_time_list
    sheet1_od['kernel execution time ratio(%)'] = kernel_exe_time_ratio_list
    sheet1_df = pd.DataFrame(sheet1_od)

    sheet2_od = collections.OrderedDict()
    sheet2_od['kernel name'] = mem_transactions_kernel_list
    sheet2_od['invocations'] = mem_transactions_invocations_list
    sheet2_od['dram_read_transactions'] = dram_read_transactions_list
    sheet2_od['dram_write_transactions'] = dram_write_transactions_list
    sheet2_df = pd.DataFrame(sheet2_od)

    sheet3_od = collections.OrderedDict()
    sheet3_od['name'] = name_list
    sheet3_od['values'] = value_list
    sheet3_df = pd.DataFrame(sheet3_od)

    excel_file_name = 'nvprof-' + str(net_name) + '-' + str(batch_size) + 'batch-fp32.xlsx'
    writer = ExcelWriter(excel_file_name)
    sheet1_df.to_excel(writer, 'Sheet1', index=False)
    sheet2_df.to_excel(writer, 'Sheet2', index=False)
    sheet3_df.to_excel(writer, 'Sheet3', index=False)
    writer.save()


if __name__ == '__main__':
    if len(sys.argv) < 6:
        sys.exit("Usage: must 6 args!")
    nvprof_log_file = sys.argv[1]
    mem_transactions_log_file = sys.argv[2]
    gpu_trace_log_file = sys.argv[3]
    net_name = sys.argv[4]
    batch_size = sys.argv[5]
    extract_flops_membwd(nvprof_log_file, mem_transactions_log_file)
    excel_io(net_name, batch_size, gpu_trace_log_file)
