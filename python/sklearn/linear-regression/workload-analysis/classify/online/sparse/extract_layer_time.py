#!/usr/bin/env python3

import sys
import re
import os
import collections
import pickle

from caffe.proto import caffe_pb2
import google.protobuf.text_format

def extract_layer_info(net_file_path):
    net_name = str(net_file_path).split('/')[0]
    if 'sparse' in net_name:
        # get sparsity
        net_name += '-'
        net_name += str(re.findall("\d+\.\d+", str(net_file_path).split('/')[1].split('-')[-1])[0])
    print(net_name)
    layer_info_dict = {}
    layer_info_dict['name'] = net_name
    net = caffe_pb2.NetParameter()
    net_file = open(net_file_path, 'r')
    net = google.protobuf.text_format.Merge(str(net_file.read()), net)
    for i in range(0, len(net.layer)):
        #print(net.layer[i].name, net.layer[i].type)
        layer_info_dict[net.layer[i].name] = net.layer[i].type
    net_file.close()
    #print(layer_info_dict)
    return layer_info_dict

def extract_layer_time(layer_time_file_path, layer_info_dict):
    file_reader = open(layer_time_file_path, 'r')
    prefix = layer_info_dict['name']
    layer_info_writer = open('layer_info.txt', 'wb')
    layer_name_writer = open(prefix + '-each_layer_time.txt', 'wb')
    layer_type_writer = open(prefix + '-layer_type_time.txt', 'wb')
    layer_name_record_dict = {}
    layer_name_round_count = {}
    layer_type_record_dict = {}
    layer_type_round_count = {}
    try:
        text_lines = file_reader.readlines()
        print(type(text_lines))
        #print(text_lines)
        for line in text_lines:
            line = line.rstrip('\n')
            line_str = line.split()
            # convert from u-second into micro-second
            layer_time = float(line_str[-2])
            layer_time /= 1000
            #print(layer_time)
            layer_name = line_str[-5]
            #print(layer_name, layer_info_dict[layer_name])
            layer_name_record_dict[layer_name] = layer_name_record_dict.get(layer_name, 0) + layer_time
            layer_name_round_count[layer_name] = layer_name_round_count.get(layer_name, 0) + 1
            layer_type_round_count[layer_info_dict[layer_name]] = layer_type_round_count.get(layer_info_dict[layer_name], 0) + 1
            layer_type_record_dict[layer_info_dict[layer_name]] = layer_type_record_dict.get(layer_info_dict[layer_name], 0) + layer_time
        case_count = layer_type_round_count.get('Accuracy')
        print("round count: ", case_count)
        for k, v in layer_name_record_dict.items():
            layer_name_record_dict[k] = v / case_count
        for k, v in layer_type_record_dict.items():
            layer_type_record_dict[k] = v / case_count
        print(layer_name_round_count)
        print(layer_type_round_count)
        print(layer_name_record_dict)
        print(layer_type_record_dict)
        pickle.dump(layer_info_dict, layer_info_writer)
        pickle.dump(layer_name_record_dict, layer_name_writer)
        pickle.dump(layer_type_record_dict, layer_type_writer)
    finally:
        file_reader.close()
        layer_info_writer.close()
        layer_name_writer.close()
        layer_type_writer.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("Usage: must 3 args!")
    net_file = sys.argv[1]
    layer_time_file = sys.argv[2]
    layer_info = extract_layer_info(net_file)
    extract_layer_time(layer_time_file, layer_info)
