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


def extract_flops_membwd(profiling_log_file, debug=True):
    nvprof_log_reader = open(profiling_log_file, 'r')
    nvprof_log_writer = open('nvprof-log.txt', 'wb')
    # key is kernel name, value is a tuple: <Invocations, flop_count_sp, dram_read_throughput, dram_write_throughput>
    flops_membwd_record_dict = {}
    try:
        lines_list = nvprof_log_reader.readlines()
        # line will be like this:
        # Invocations   Metric Name     Metric Description   Min     Max     Avg
        for i, line in enumerate(lines_list):
            if 'Kernel' in line:
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
        if debug:
            print(flops_membwd_record_dict)
        pickle.dump(flops_membwd_record_dict, nvprof_log_writer)
    finally:
        nvprof_log_reader.close()
        nvprof_log_writer.close()

def excel_io(net_name, batch_size, debug=True):
    nvprof_flops_membwd_reader = open('nvprof-log.txt', 'rb')
    flops_membwd_record_dict = pickle.load(nvprof_flops_membwd_reader)
    if debug:
        print(flops_membwd_record_dict)

    kernel_list = []
    invocations_list = []
    flop_count_sp_list = []
    dram_read_throughput_list = []
    dram_write_throughput_list = []

    try:
        for k, v in flops_membwd_record_dict.items():
            kernel_list.append(k)
            invocations_list.append(int(v[0]))
            flop_count_sp_list.append(int(v[1]))
            dram_read_throughput_list.append(float(v[2]))
            dram_write_throughput_list.append(float(v[3]))

    finally:
        nvprof_flops_membwd_reader.close()

    assert len(kernel_list) == len(invocations_list) and \
            len(invocations_list) == len(flop_count_sp_list) and \
            len(flop_count_sp_list) == len(dram_read_throughput_list) and \
            len(dram_read_throughput_list) == len(dram_write_throughput_list), \
            " Error! Must have same records length!"

    sheet1_od = collections.OrderedDict()
    sheet1_od['kernel name'] = kernel_list
    sheet1_od['invocations'] = invocations_list
    sheet1_od['flop_count_sp'] = flop_count_sp_list
    sheet1_od['dram_read_throughput(GB/s)'] = dram_read_throughput_list
    sheet1_od['dram_write_throughput_list(GB/s)'] = dram_write_throughput_list
    sheet1_df = pd.DataFrame(sheet1_od)

    excel_file_name = 'nvprof-' + str(net_name) + '-' + str(batch_size) + 'batch-fp32.xlsx'
    writer = ExcelWriter(excel_file_name)
    sheet1_df.to_excel(writer, 'Sheet1', index=False)
    writer.save()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit("Usage: must 4 args!")
    nvprof_log_file = sys.argv[1]
    net_name = sys.argv[2]
    batch_size = sys.argv[3]
    extract_flops_membwd(nvprof_log_file)
    excel_io(net_name, batch_size)
