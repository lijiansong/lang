#!/usr/bin/env python3

import sys
import re
import os

def extract_end2end_fps(end2end_file_path):
    file_reader = open(end2end_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-end2end_fps.txt', 'w')
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            print(line_str)
            end2end_fps = float(line_str[3])
            _, _, _, batch_size, data_parallel, model_parallel, thread_num = line_str[0].split("-")
            batch_size = re.findall(r'\d+', batch_size)
            res = batch_size[0] + ',' + data_parallel + ',' + model_parallel + ',' + thread_num + ',' + str(end2end_fps) + '\n'
            print(res)
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

def extract_hardware_fps(hw_fps_file_path):
    file_reader = open(hw_fps_file_path, 'r')
    prefix = os.getcwd().split("/")[-2]
    file_writer = open(prefix + '-hardware_fps.txt', 'w')
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            #print(line)
            line_str = line.split(":", 3)
            print(line_str)
            end2end_fps = float(line_str[3])
            _, _, _, batch_size, data_parallel, model_parallel, thread_num = line_str[0].split("-")
            batch_size = re.findall(r'\d+', batch_size)
            res = batch_size[0] + ',' + data_parallel + ',' + model_parallel + ',' + thread_num + ',' + str(end2end_fps) + '\n'
            print(res)
            file_writer.write(res)
    finally:
        file_reader.close()
        file_writer.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("Usage: must 3 args!")
    end2end_file = sys.argv[1]
    hw_fps_file = sys.argv[2]
    extract_end2end_fps(end2end_file)
    extract_hardware_fps(hw_fps_file)
