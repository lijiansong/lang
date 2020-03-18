#!/usr/bin/env python3

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
    # key is kernel name, value is a tuple: <Invocations, flop_count_sp, dram_read_throughput, dram_write_throughput>
    flops_membwd_record_dict = {}
    mem_transactions_record_dict = {}
    try:
        lines_list = nvprof_log_reader.readlines()
        # line will be like this:
        # Invocations   Metric Name     Metric Description   Min     Max     Avg
        for i, line in enumerate(lines_list):
            if 'Kernel:' in line:
                # 1. extract the kernel name
                kernel_name = ''
                for item in line.split()[1:]:
                    kernel_name += item
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
                kernel_name = ''
                for item in line.split()[1:]:
                    kernel_name += item
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
        pickle.dump(flops_membwd_record_dict, nvprof_log_writer)
        pickle.dump(mem_transactions_record_dict, mem_transactions_writer)
    finally:
        nvprof_log_reader.close()
        mem_transactions_log_reader.close()
        nvprof_log_writer.close()
        mem_transactions_writer.close()

def excel_io(net_name, batch_size, debug=True):
    nvprof_flops_membwd_reader = open('nvprof-log.txt', 'rb')
    nvprof_mem_transactions_reader = open('nvprof-mem-transactions.txt', 'rb')
    flops_membwd_record_dict = pickle.load(nvprof_flops_membwd_reader)
    mem_transactions_record_dict = pickle.load(nvprof_mem_transactions_reader)
    if debug:
        print(flops_membwd_record_dict)
        print(mem_transactions_record_dict)

    kernel_list = []
    invocations_list = []
    flop_count_sp_list = []
    dram_read_throughput_list = []
    dram_write_throughput_list = []

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
    total_invocations = 0
    for item in invocations_list:
        total_invocations += item
    total_flop_count_sp = 0
    avg_dram_read_throughput = 0
    avg_dram_write_throughput = 0
    for i, invos in enumerate(invocations_list):
        total_flop_count_sp += flop_count_sp_list[i] * invos
        avg_dram_read_throughput += (dram_read_throughput_list[i] * invos / total_invocations)
        avg_dram_write_throughput += (dram_write_throughput_list[i] * invos / total_invocations)

    # calculate the average dram_read_transactions, dram_write_transactions
    total_invocations = 0
    avg_dram_read_transactions = 0
    avg_dram_write_transactions = 0
    for item in mem_transactions_invocations_list:
        total_invocations += item
    for i, invos in enumerate(mem_transactions_invocations_list):
        avg_dram_read_transactions += (dram_read_transactions_list[i] * invos) / total_invocations
        avg_dram_write_transactions += (dram_write_transactions_list[i] * invos) / total_invocations

    value_list = [total_flop_count_sp, avg_dram_read_throughput, avg_dram_write_throughput, avg_dram_read_transactions, avg_dram_write_transactions]
    name_list = ['total_flop_count_sp', 'avg_dram_read_throughput', 'avg_dram_write_throughput', 'avg_dram_read_transactions', 'avg_dram_write_transactions']


    sheet1_od = collections.OrderedDict()
    sheet1_od['kernel name'] = kernel_list
    sheet1_od['invocations'] = invocations_list
    sheet1_od['flop_count_sp'] = flop_count_sp_list
    sheet1_od['dram_read_throughput(GB/s)'] = dram_read_throughput_list
    sheet1_od['dram_write_throughput_list(GB/s)'] = dram_write_throughput_list
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
    if len(sys.argv) < 5:
        sys.exit("Usage: must 5 args!")
    nvprof_log_file = sys.argv[1]
    mem_transactions_log_file = sys.argv[2]
    net_name = sys.argv[3]
    batch_size = sys.argv[4]
    extract_flops_membwd(nvprof_log_file, mem_transactions_log_file)
    excel_io(net_name, batch_size)
