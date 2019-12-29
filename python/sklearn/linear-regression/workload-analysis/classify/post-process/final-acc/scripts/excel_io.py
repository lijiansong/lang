#!/usr/bin/env python3

import sys
import re
import os
import collections
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

def extract_into_excel():
    '''
    Dependency contains pandas and openpyxl.
    If you are using python3 @ Ubuntu, then:
    apt install python3-pandas
    apt install python3-xlsxwriter
    '''
    # TODO: this coding style is very ugly.
    prefix = os.getcwd().split("/")[-2]
    end2end_fps_file = prefix + '-end2end_fps.txt'
    hardware_fps_file = prefix + '-hardware_fps.txt'
    total_exe_time_file = prefix + '-total-exe-time.txt'
    final_acc_file = prefix + '-global-acc.txt'

    sparsity_list = []
    batch_size_list = []
    data_parallel_list = []
    model_parallel_list = []
    thread_num_list = []
    fifo_size_list = []
    end2end_fps_list = []
    hardware_fps_list = []
    total_exe_time_list = []
    final_acc_list = []

    # end to end fps
    file_reader = open(end2end_fps_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(text_lines)
        for line in text_lines:
            sparsity, batch_size, data_parallel, model_parallel, thread_num, end2end_fps = line.split(",")
            sparsity_list.append(float(sparsity))
            batch_size_list.append(int(batch_size))
            data_parallel_list.append(int(data_parallel))
            model_parallel_list.append(int(model_parallel))
            thread_num_list.append(int(thread_num))
            fifo_size_list.append(2)
            end2end_fps_list.append(float(end2end_fps))
    finally:
        file_reader.close()

    # hardware fps
    file_reader = open(hardware_fps_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, hardware_fps = line.split(",")
            hardware_fps_list.append(float(hardware_fps))
    finally:
        file_reader.close()

    # total exe time
    file_reader = open(total_exe_time_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, total_exe_time = line.split(",")
            total_exe_time_list.append(float(total_exe_time))
    finally:
        file_reader.close()

    # final top-1 accuracy
    file_reader = open(final_acc_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, final_acc = line.split(",")
            final_acc_list.append(float(final_acc))
    finally:
        file_reader.close()

    assert len(sparsity_list) == len(batch_size_list) and \
            len(batch_size_list) == len(data_parallel_list) and \
            len(data_parallel_list) == len(model_parallel_list) and \
            len(model_parallel_list) == len(thread_num_list) and \
            len(thread_num_list) == len(fifo_size_list) and \
            len(fifo_size_list) == len(end2end_fps_list) and \
            len(end2end_fps_list) == len(hardware_fps_list) and \
            len(hardware_fps_list) == len(total_exe_time_list) and \
            len(total_exe_time_list) == len(final_acc_list), \
            " Error! Must have same records length!"
    ordered_dict = collections.OrderedDict()
    ordered_dict['sparsity'] = sparsity_list
    ordered_dict['batch size'] = batch_size_list
    ordered_dict['data parallel'] = data_parallel_list
    ordered_dict['model parallel'] = model_parallel_list
    ordered_dict['thread num'] = thread_num_list
    ordered_dict['fifo size'] = fifo_size_list
    ordered_dict['end to end FPS'] = end2end_fps_list
    ordered_dict['hardware FPS'] = hardware_fps_list
    ordered_dict['total execution time(ms)'] = total_exe_time_list
    ordered_dict['top-1 accuracy'] = final_acc_list
    df = pd.DataFrame(ordered_dict)
    excel_file_name = prefix + '.xlsx'
    writer = ExcelWriter(excel_file_name)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

if __name__ == '__main__':
    extract_into_excel()
