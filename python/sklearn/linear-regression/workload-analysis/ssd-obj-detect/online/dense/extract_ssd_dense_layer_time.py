#!/usr/bin/env python3

import sys
import re
import os
import collections
import pickle

from caffe.proto import caffe_pb2
import google.protobuf.text_format
import caffe

def extract_layer_info(net_file_path):
    net_name = str(net_file_path).split('.')[0]
    tmp = net_name.split('_')[0:2]
    if 'int8' in net_name:
        # get sparsity
        net_name = str(tmp[0]) + '_' + str(tmp[1])
        net_name += '-dense-int8'
    else:
        net_name = str(tmp[0]) + '_' + str(tmp[1])
        net_name += '-dense-fp16'
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

# FIXME: remove redundant func 'extract_layer_info'
def extract_layer_shape(net_file_path):
    # read the net and weight
    #net = caffe.Net(net_file_path, weight_file_path, caffe.TEST)
    # only read the net
    net = caffe.Net(net_file_path, caffe.TEST)
    net_shape_dict = {}
    for li in xrange(len(net.layers)):
        # store layer's information
        layer = {}
        layer_name = net._layer_names[li]
        # for each input to the layer (aka "bottom") store its shape(type tuple)
        layer['bottoms'] = [net.blobs[net._blob_names[bi]].data.shape
                             for bi in list(net._bottom_ids(li))]
        # for each output of the layer (aka "top") store its shape
        layer['tops'] = [(net.blobs[net._blob_names[bi]].data.shape)
                          for bi in list(net._top_ids(li))]
        # the internal parameters of the layer, not all layers has weights.
        #layer['weights'] = [net.layers[li].blobs[bi].data[...]
        #                    for bi in xrange(len(net.layers[li].blobs))]
        # type of the layer
        layer['type'] = net.layers[li].type
        #print(layer)
        net_shape_dict[layer_name] = layer

    # get the parameters of 'Convolution' and 'Pooling' layers
    parsible_net = caffe_pb2.NetParameter()
    google.protobuf.text_format.Merge(open(net_file_path).read(), parsible_net)
    for layer in parsible_net.layer:
        if layer.type == 'Convolution':
            #print('Convolution')
            #print('kernel_size:', layer.convolution_param.kernel_size[0] if len(layer.convolution_param.kernel_size) else 1)
            #print('stride:', layer.convolution_param.stride[0] if len(layer.convolution_param.stride) else 1)
            #print('pad:', layer.convolution_param.pad[0] if len(layer.convolution_param.pad) else 0)
            net_shape_dict[layer.name]['kernel_size'] = layer.convolution_param.kernel_size[0] if len(layer.convolution_param.kernel_size) else 1
            net_shape_dict[layer.name]['stride'] = layer.convolution_param.stride[0] if len(layer.convolution_param.stride) else 1
            net_shape_dict[layer.name]['pad'] = layer.convolution_param.pad[0] if len(layer.convolution_param.pad) else 0
        if layer.type == 'Pooling':
            #print('Pooling')
            #print('kernel size:', layer.pooling_param.kernel_size)
            #print('stride:', layer.pooling_param.stride)
            #print('pad:', layer.pooling_param.pad)
            net_shape_dict[layer.name]['kernel_size'] = layer.pooling_param.kernel_size
            net_shape_dict[layer.name]['stride'] = layer.pooling_param.stride
            net_shape_dict[layer.name]['pad'] = layer.pooling_param.pad
    return net_shape_dict

def extract_layer_time(layer_time_file_path, layer_info_dict, layer_shape_dict):
    file_reader = open(layer_time_file_path, 'r')
    prefix = layer_info_dict['name']
    layer_info_writer = open('layer_info.txt', 'wb')
    layer_shape_writer = open('layer_shape.txt', 'wb')
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
            print(line_str)
            layer_name = line_str[-5]
            #print(layer_name, layer_info_dict[layer_name])
            if layer_info_dict[layer_name] == 'Input':
                continue
            layer_name_record_dict[layer_name] = layer_name_record_dict.get(layer_name, 0) + layer_time
            layer_name_round_count[layer_name] = layer_name_round_count.get(layer_name, 0) + 1
            layer_type_round_count[layer_info_dict[layer_name]] = layer_type_round_count.get(layer_info_dict[layer_name], 0) + 1
            layer_type_record_dict[layer_info_dict[layer_name]] = layer_type_record_dict.get(layer_info_dict[layer_name], 0) + layer_time
        case_count = layer_type_round_count.get('SsdDetection')
        print("round count: ", case_count)
        for k, v in layer_name_record_dict.items():
            layer_name_record_dict[k] = v / case_count
            if layer_info_dict[k] == 'Input' or layer_info_dict[k] == 'Accuracy':
                del layer_name_record_dict[k]
        for k, v in layer_type_record_dict.items():
            layer_type_record_dict[k] = v / case_count
            if k == 'Input' or k == 'Accuracy':
                del layer_type_record_dict[k]
        print(layer_name_round_count)
        print(layer_type_round_count)
        print(layer_name_record_dict)
        print(layer_type_record_dict)
        pickle.dump(layer_info_dict, layer_info_writer)
        pickle.dump(layer_shape_dict, layer_shape_writer)
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
    layer_shape = extract_layer_shape(net_file)
    extract_layer_time(layer_time_file, layer_info, layer_shape)
