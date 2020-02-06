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

    prepare_input_time_file = prefix + '-prepare_input.txt'
    copyin_time_file = prefix + '-copyin_time.txt'
    execution_time_file = prefix + '-execution_time.txt'
    copyout_time_file = prefix + '-copyout_time.txt'
    post_process_time_file = prefix + '-post_process_time.txt'

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

    prepare_input_time_list = []
    copyin_time_list = []
    execution_time_list = []
    copyout_time_list = []
    post_process_time_list = []

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

    # prepare input time
    file_reader = open(prepare_input_time_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, _, _, _, _, prepare_input_time = line.split(",")
            prepare_input_time_list.append(float(prepare_input_time))
    finally:
        file_reader.close()

    # copyin time
    file_reader = open(copyin_time_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, _, _, _, _, copyin_time = line.split(",")
            copyin_time_list.append(float(copyin_time))
    finally:
        file_reader.close()

    # execution time
    file_reader = open(execution_time_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, _, _, _, _, execution_time = line.split(",")
            execution_time_list.append(float(execution_time))
    finally:
        file_reader.close()

    # copyout time
    file_reader = open(copyout_time_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, _, _, _, _, copyout_time = line.split(",")
            copyout_time_list.append(float(copyout_time))
    finally:
        file_reader.close()

    # post process time
    file_reader = open(post_process_time_file, 'r')
    try:
        text_lines = file_reader.readlines()
        #print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            _, _, _, _, _, post_process_time = line.split(",")
            post_process_time_list.append(float(post_process_time))
    finally:
        file_reader.close()

    assert len(batch_size_list) == len(data_parallel_list) and \
            len(data_parallel_list) == len(model_parallel_list) and \
            len(model_parallel_list) == len(thread_num_list) and \
            len(thread_num_list) == len(fifo_size_list) and \
            len(fifo_size_list) == len(end2end_fps_list) and \
            len(end2end_fps_list) == len(hardware_fps_list) and \
            len(hardware_fps_list) == len(total_exe_time_list) and \
            len(total_exe_time_list) == len(prepare_input_time_list) and \
            len(prepare_input_time_list) == len(copyin_time_list) and \
            len(copyin_time_list) == len(execution_time_list) and \
            len(execution_time_list) == len(copyout_time_list) and \
            len(copyout_time_list) == len(post_process_time_list), \
            " Error! Must have same records length!"

    ordered_dict = collections.OrderedDict()
    ordered_dict['sparsity'] = sparsity_list
    ordered_dict['batch size'] = batch_size_list
    ordered_dict['data parallel'] = data_parallel_list
    ordered_dict['model parallel'] = model_parallel_list
    ordered_dict['thread num'] = thread_num_list
    ordered_dict['fifo size'] = fifo_size_list
    ordered_dict['End to end FPS'] = end2end_fps_list
    ordered_dict['Hardware FPS'] = hardware_fps_list
    ordered_dict['Total execution time(ms)'] = total_exe_time_list
    ordered_dict['Top-1 accuracy'] = final_acc_list
    ordered_dict['Prepare input time(ms)'] = prepare_input_time_list
    ordered_dict['Copyin time(ms)'] = copyin_time_list
    ordered_dict['Execution time(ms)'] = execution_time_list
    ordered_dict['Copyout time(ms)'] = copyout_time_list
    ordered_dict['Post process time(ms)'] = post_process_time_list
    df = pd.DataFrame(ordered_dict)
    excel_file_name = prefix + '.xlsx'
    writer = ExcelWriter(excel_file_name)
    df.to_excel(writer,'Sheet1',index=False)
    writer.save()

if __name__ == '__main__':
    extract_into_excel()
