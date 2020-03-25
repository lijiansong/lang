#!/usr/bin/env python3

import sys
import re
import os
import collections
import pickle

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

def unpack_layer_tops_product(layer_top):
    product = 1
    for i in layer_top:
        product *= int(i)
    return product

def calculate_mlu_ops_byte(layer_name, net_shape_dict, debug=True):
    flops = 0
    mem_bytes = 0
    if debug:
        print(net_shape_dict)
    if layer_name in net_shape_dict:
        v = net_shape_dict[layer_name]
        if v['type'] == 'Convolution':
            # ops = out_h*out_w*(2*in_c*k_s*k_s)*out_c*out_n
            # bytes = (k_s*k_s*in_c*out_c+out_h*out_w*out_c)*out_n*2
            in_n, in_c, in_h, in_w = v['bottoms'][0]
            out_n, out_c, out_h, out_w = v['tops'][0]
            k_s = int(v['kernel_size'])
            in_n, in_c, in_h, in_w = int(in_n), int(in_c), int(in_h), int(in_w)
            out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            flops = out_h * out_w * (2 * in_c * k_s * k_s) * out_c * out_n
            mem_bytes = (k_s * k_s * in_c * out_c + out_h * out_w * out_c) * out_n * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'Pooling':
            in_n, in_c, in_h, in_w = v['bottoms'][0]
            out_n, out_c, out_h, out_w = v['tops'][0]
            k_s = int(v['kernel_size'])
            in_n, in_c, in_h, in_w = int(in_n), int(in_c), int(in_h), int(in_w)
            out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            if int(v['kernel_size']) == 0:
                # global pooling
                # ops = in_c*in_h*in_w*in_n or in_c*(in_h*in_w+1)*in_n
                # bytes = (in_c*in_h*in_w+out_c*out_h*out_w)*out_n*2
                flops = in_c * (in_h * in_w + 1) * in_n
                mem_bytes = (in_c * in_h * in_w + out_c * out_h * out_w) * out_n * 2
            else:
                # common pooling
                # ops = out_c*out_h*out_w*k_s*k_s*out_n
                # bytes = out_c*out_h*out_w*(k_s*k_s+1)*out_n*2
                flops = out_c * out_h * out_w * k_s * k_s * out_n
                mem_bytes = out_c * out_h * out_w * (k_s * k_s + 1) * out_n * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'ReLU':
            # ops=2*N*C*H*W
            # bytes=2*N*C*H*W*2
            out_n, out_c, out_h, out_w = v['tops'][0]
            out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            flops = 2 * out_n * out_c * out_h * out_w
            mem_bytes = 2 * out_n * out_c * out_w * out_w * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'Scale':
            # ops=2*N*C*H*W
            # bytes=3*N*C*H*W*2
            #out_n, out_c, out_h, out_w = v['tops'][0]
            #out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            #flops = 2 * out_n * out_c * out_h * out_w
            #mem_bytes = 3 * out_n * out_c * out_w * out_w * 2
            product = unpack_layer_tops_product(v['tops'][0])
            flops = 2 * product
            mem_bytes = 3 * product * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'Softmax':
            # ops=4*N*C*H*W
            # bytes=2*N*C*H*W*2
            # Note: sometimes this layer only has two dimensions:
            product = unpack_layer_tops_product(v['tops'][0])
            flops = 4 * product
            mem_bytes = 2 * product * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'BatchNorm':
            # ops=8*N*C*H*W
            # bytes=4*N*C*H*W*2
            #out_n, out_c, out_h, out_w = v['tops'][0]
            #out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            #flops = 8 * out_n * out_c * out_h * out_w
            #mem_bytes = 4 * out_n * out_c * out_w * out_w * 2
            product = unpack_layer_tops_product(v['tops'][0])
            flops = 8 * product
            mem_bytes = 4 * product * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'Dropout':
            # ops=3*N*C*H*W
            # bytes=3*N*C*H*W*2
            out_n, out_c, out_h, out_w = v['tops'][0]
            out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            flops = 3 * out_n * out_c * out_h * out_w
            mem_bytes = 3 * out_n * out_c * out_w * out_w * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'Concat':
            # ops=0
            # bytes=2*out_n*out*c*out*h*out*w*2
            out_n, out_c, out_h, out_w = v['tops'][0]
            out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            flops = 0
            mem_bytes = 2 * out_n * out_c * out_w * out_w * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'Eltwise':
            # ops=2*N*C*H*W
            # bytes=3*N*C*H*W*2
            #out_n, out_c, out_h, out_w = v['tops'][0]
            #out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            #flops = 2 * out_n * out_c * out_h * out_w
            #mem_bytes = 3 * out_n * out_c * out_w * out_w * 2
            product = unpack_layer_tops_product(v['tops'][0])
            flops = 2 * product
            mem_bytes = 3 * product * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'InnerProduct':
            # ops = out_h*outw*(2*in_c*k_s*k_s)*out_c*out_n
            # bytes = (k_s*k_s*in_c*out_c+out_h*out_w*out_c)*in_n*2
            if debug:
                print('bottoms: ', v['bottoms'])
                print('tops: ', v['tops'])
            in_n, in_c, in_h, in_w = v['bottoms'][0]
            #out_n, out_c, out_h, out_w = v['tops'][0]
            if len(v['tops'][0]) == 4:
                out_n, out_c, out_h, out_w = v['tops'][0]
            elif len(v['tops'][0]) == 3:
                out_n, out_c, out_h = v['tops'][0]
                out_w = 1
            elif len(v['tops'][0]) == 2:
                out_n, out_c = v['tops'][0]
                out_h = 1
                out_w = 1
            elif len(v['tops'][0]) == 1:
                out_n = v['tops'][0]
                out_c = 1
                out_h = 1
                out_w = 1
            if 'kernel_size' in v:
                k_s = int(v['kernel_size'])
            else:
                k_s = 1
            in_n, in_c, in_h, in_w = int(in_n), int(in_c), int(in_h), int(in_w)
            flops = out_h * out_w * (2 * in_c * k_s * k_s) * out_c * out_n
            mem_bytes = (k_s * k_s * in_c * out_c + out_h * out_w * out_c) * in_n * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'Normalize':
            # ops=8*N*C*H*W
            # bytes=2*N*C*H*W*2
            out_n, out_c, out_h, out_w = v['tops'][0]
            out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            flops = 8 * out_n * out_c * out_h * out_w
            mem_bytes = 2 * out_n * out_c * out_w * out_w * 2
            if debug:
                print(flops, mem_bytes)
        elif v['type'] == 'SsdDetection':
            # ops=4*N*C*H*W
            # bytes=(in_0+in_1+...+in_n+out)*2
            out_n, out_c, out_h, out_w = v['tops'][0]
            out_n, out_c, out_h, out_w = int(out_n), int(out_c), int(out_h), int(out_w)
            flops = 4 * out_n * out_c * out_h * out_w
            mem_bytes = 0
            for n, c, h, w in v['bottoms']:
                mem_bytes +=  n * c * h * w * 2
            mem_bytes += out_n * out_c * out_h * out_w * 2
            if debug:
                print(flops, mem_bytes)
    return flops, mem_bytes

def extract_into_excel(layer_info_file='layer_info.txt', layer_shape_file='layer_shape.txt', debug=False):
    layer_info_reader = open(layer_info_file, 'rb')
    layer_info = pickle.load(layer_info_reader)
    net_name = layer_info['name']
    print(net_name)
    layer_shape_reader = open(layer_shape_file, 'rb')
    layer_shape = pickle.load(layer_shape_reader)

    layer_name_time_reader = open(str(net_name) + '-each_layer_time.txt', 'rb')
    layer_type_time_reader = open(str(net_name) + '-layer_type_time.txt', 'rb')

    layer_name_record_dict = pickle.load(layer_name_time_reader)
    layer_type_record_dict = pickle.load(layer_type_time_reader)

    layer_name_list = []
    layer_name_type_list = []
    layer_name_time_list = []
    layer_type_list = []
    layer_type_time_list = []

    max_bottoms_length = max_tops_length = 0
    # multiple input and output shape info
    layer_shape_list_dict = {}
    kernel_size_list = []
    stride_list = []
    pad_list = []

    try:
        for k, v in list(layer_shape.items()):
            if v['type'] == 'Data' or v['type'] == 'Accuracy':
                del layer_shape[k]
                continue
            max_bottoms_length = max(max_bottoms_length, len(v['bottoms']))
            max_tops_length = max(max_tops_length, len(v['tops']))
        # determine the input and output tuples length
        for i in range(0, max_bottoms_length):
            layer_shape_list_dict['Input' + str(i) + ' N'] = []
            layer_shape_list_dict['Input' + str(i) + ' C'] = []
            layer_shape_list_dict['Input' + str(i) + ' H'] = []
            layer_shape_list_dict['Input' + str(i) + ' W'] = []
        for i in range(0, max_tops_length):
            layer_shape_list_dict['Output' + str(i) + ' N'] = []
            layer_shape_list_dict['Output' + str(i) + ' C'] = []
            layer_shape_list_dict['Output' + str(i) + ' H'] = []
            layer_shape_list_dict['Output' + str(i) + ' W'] = []

        for k, v in layer_name_record_dict.items():
            layer_name_list.append(str(k))
            layer_name_type_list.append(str(layer_info[str(k)]))
            layer_name_time_list.append(float(v))
            # 'kernel_size', 'stride', 'pad'
            if layer_info[str(k)] == 'Convolution' or layer_info[str(k)] == 'Pooling':
                kernel_size_list.append(int(layer_shape[str(k)]['kernel_size']))
                stride_list.append(int(layer_shape[str(k)]['stride']))
                pad_list.append(int(layer_shape[str(k)]['pad']))
            else:
                kernel_size_list.append(float('nan'))
                stride_list.append(float('nan'))
                pad_list.append(float('nan'))
            # Input and output shape
            for i in range(0, len(layer_shape[str(k)]['bottoms'])):
                if debug:
                    print('max tops len:', max_tops_length, 'max bottoms len:', max_bottoms_length)
                    print('layer:', str(k), 'type:', layer_shape[str(k)]['type'], 'bottoms:', layer_shape[str(k)]['bottoms'][i])
                if len(layer_shape[str(k)]['bottoms'][i]) == 1:
                    layer_shape_list_dict['Input' + str(i) + ' N'].append(int(layer_shape[str(k)]['bottoms'][i][0]))
                    layer_shape_list_dict['Input' + str(i) + ' C'].append(float('nan'))
                    layer_shape_list_dict['Input' + str(i) + ' H'].append(float('nan'))
                    layer_shape_list_dict['Input' + str(i) + ' W'].append(float('nan'))
                elif len(layer_shape[str(k)]['bottoms'][i]) == 2:
                    layer_shape_list_dict['Input' + str(i) + ' N'].append(int(layer_shape[str(k)]['bottoms'][i][0]))
                    layer_shape_list_dict['Input' + str(i) + ' C'].append(int(layer_shape[str(k)]['bottoms'][i][1]))
                    layer_shape_list_dict['Input' + str(i) + ' H'].append(float('nan'))
                    layer_shape_list_dict['Input' + str(i) + ' W'].append(float('nan'))
                elif len(layer_shape[str(k)]['bottoms'][i]) == 3:
                    layer_shape_list_dict['Input' + str(i) + ' N'].append(int(layer_shape[str(k)]['bottoms'][i][0]))
                    layer_shape_list_dict['Input' + str(i) + ' C'].append(int(layer_shape[str(k)]['bottoms'][i][1]))
                    layer_shape_list_dict['Input' + str(i) + ' H'].append(int(layer_shape[str(k)]['bottoms'][i][2]))
                    layer_shape_list_dict['Input' + str(i) + ' W'].append(float('nan'))
                elif len(layer_shape[str(k)]['bottoms'][i]) == 4:
                    layer_shape_list_dict['Input' + str(i) + ' N'].append(int(layer_shape[str(k)]['bottoms'][i][0]))
                    layer_shape_list_dict['Input' + str(i) + ' C'].append(int(layer_shape[str(k)]['bottoms'][i][1]))
                    layer_shape_list_dict['Input' + str(i) + ' H'].append(int(layer_shape[str(k)]['bottoms'][i][2]))
                    layer_shape_list_dict['Input' + str(i) + ' W'].append(int(layer_shape[str(k)]['bottoms'][i][3]))
            for i in range(len(layer_shape[str(k)]['bottoms']), max_bottoms_length):
                layer_shape_list_dict['Input' + str(i) + ' N'].append(float('nan'))
                layer_shape_list_dict['Input' + str(i) + ' C'].append(float('nan'))
                layer_shape_list_dict['Input' + str(i) + ' H'].append(float('nan'))
                layer_shape_list_dict['Input' + str(i) + ' W'].append(float('nan'))

            for i in range(0, len(layer_shape[str(k)]['tops'])):
                if len(layer_shape[str(k)]['tops'][i]) == 1:
                    layer_shape_list_dict['Output' + str(i) + ' N'].append(int(layer_shape[str(k)]['tops'][i][0]))
                    layer_shape_list_dict['Output' + str(i) + ' C'].append(float('nan'))
                    layer_shape_list_dict['Output' + str(i) + ' H'].append(float('nan'))
                    layer_shape_list_dict['Output' + str(i) + ' W'].append(float('nan'))
                elif len(layer_shape[str(k)]['tops'][i]) == 2:
                    layer_shape_list_dict['Output' + str(i) + ' N'].append(int(layer_shape[str(k)]['tops'][i][0]))
                    layer_shape_list_dict['Output' + str(i) + ' C'].append(int(layer_shape[str(k)]['tops'][i][1]))
                    layer_shape_list_dict['Output' + str(i) + ' H'].append(float('nan'))
                    layer_shape_list_dict['Output' + str(i) + ' W'].append(float('nan'))
                elif len(layer_shape[str(k)]['tops'][i]) == 3:
                    layer_shape_list_dict['Output' + str(i) + ' N'].append(int(layer_shape[str(k)]['tops'][i][0]))
                    layer_shape_list_dict['Output' + str(i) + ' C'].append(int(layer_shape[str(k)]['tops'][i][1]))
                    layer_shape_list_dict['Output' + str(i) + ' H'].append(int(layer_shape[str(k)]['tops'][i][2]))
                    layer_shape_list_dict['Output' + str(i) + ' W'].append(float('nan'))
                elif len(layer_shape[str(k)]['tops'][i]) == 4:
                    layer_shape_list_dict['Output' + str(i) + ' N'].append(int(layer_shape[str(k)]['tops'][i][0]))
                    layer_shape_list_dict['Output' + str(i) + ' C'].append(int(layer_shape[str(k)]['tops'][i][1]))
                    layer_shape_list_dict['Output' + str(i) + ' H'].append(int(layer_shape[str(k)]['tops'][i][2]))
                    layer_shape_list_dict['Output' + str(i) + ' W'].append(int(layer_shape[str(k)]['tops'][i][3]))
            for i in range(len(layer_shape[str(k)]['tops']), max_tops_length):
                if debug:
                    print('max tops len:', max_tops_length, 'max bottoms len:', max_bottoms_length)
                    print('layer:', str(k), 'type:', layer_shape[str(k)]['type'], 'tops:', layer_shape[str(k)]['tops'])
                layer_shape_list_dict['Output' + str(i) + ' N'].append(float('nan'))
                layer_shape_list_dict['Output' + str(i) + ' C'].append(float('nan'))
                layer_shape_list_dict['Output' + str(i) + ' H'].append(float('nan'))
                layer_shape_list_dict['Output' + str(i) + ' W'].append(float('nan'))

        for k, v in layer_type_record_dict.items():
            layer_type_list.append(str(k))
            layer_type_time_list.append(float(v))

    finally:
        layer_info_reader.close()
        layer_shape_reader.close()
        layer_name_time_reader.close()
        layer_type_time_reader.close()

    assert len(layer_name_list) == len(layer_name_time_list) and \
            len(layer_name_time_list) == len(kernel_size_list) and \
            len(kernel_size_list) == len(stride_list) and \
            len(stride_list) == len(pad_list) and \
            len(layer_type_list) == len(layer_type_time_list), \
            " Error! Must have same records length!"
    # calculate flops and memory accessing bytes
    ops_list = []
    mem_bytes_list = []
    for layer_name in layer_name_list:
        flops, mem_bytes = calculate_mlu_ops_byte(layer_name, layer_shape)
        ops_list.append(flops)
        mem_bytes_list.append(mem_bytes)

    gflops_list = []
    intensity_list = []
    total_model_ops = 0.0
    total_model_mem_bytes = 0.0
    for i, exe_time in enumerate(layer_name_time_list):
        gflops_list.append(ops_list[i] / 1e9 / (exe_time / 1e3))
        intensity_list.append(float(ops_list[i] / mem_bytes_list[i]))
        total_model_ops += ops_list[i]
        total_model_mem_bytes += mem_bytes_list[i]

    avg_model_intensity = float(total_model_ops / total_model_mem_bytes)
    total_model_time = 0
    for time in layer_type_time_list:
        total_model_time += time
    avg_model_gflops = total_model_ops / 1e9 / (total_model_time / 1e3)

    # for sheet3 columns
    value_list = [total_model_ops, total_model_mem_bytes, total_model_time, avg_model_gflops, avg_model_intensity]
    name_list = ['model ops', 'model bytes', 'model time(ms)', 'model GFLOPS', 'model intensity']

    sheet1_od = collections.OrderedDict()
    sheet1_od['layer name'] = layer_name_list
    sheet1_od['layer type'] = layer_name_type_list
    sheet1_od['time(ms)'] = layer_name_time_list
    sheet1_od['Ops'] = ops_list
    sheet1_od['Bytes'] = mem_bytes_list
    sheet1_od['GFLOPS'] = gflops_list
    sheet1_od['Intensity'] = intensity_list
    for i in range(0, max_bottoms_length):
        sheet1_od['Input' + str(i) + ' N'] = layer_shape_list_dict['Input' + str(i) + ' N']
        sheet1_od['Input' + str(i) + ' C'] = layer_shape_list_dict['Input' + str(i) + ' C']
        sheet1_od['Input' + str(i) + ' H'] = layer_shape_list_dict['Input' + str(i) + ' H']
        sheet1_od['Input' + str(i) + ' W'] = layer_shape_list_dict['Input' + str(i) + ' W']
    sheet1_od['kernel size'] = kernel_size_list
    sheet1_od['stride'] = stride_list
    sheet1_od['pad'] = pad_list
    for i in range(0, max_tops_length):
        sheet1_od['Output' + str(i) + ' N'] = layer_shape_list_dict['Output' + str(i) + ' N']
        sheet1_od['Output' + str(i) + ' C'] = layer_shape_list_dict['Output' + str(i) + ' C']
        sheet1_od['Output' + str(i) + ' H'] = layer_shape_list_dict['Output' + str(i) + ' H']
        sheet1_od['Output' + str(i) + ' W'] = layer_shape_list_dict['Output' + str(i) + ' W']
    sheet1_df = pd.DataFrame(sheet1_od)

    sheet2_od = collections.OrderedDict()
    sheet2_od['layer type'] = layer_type_list
    sheet2_od['time(ms)'] = layer_type_time_list
    sheet2_df = pd.DataFrame(sheet2_od)

    sheet3_od = collections.OrderedDict()
    sheet3_od['name'] = name_list
    sheet3_od['value'] = value_list
    sheet3_df = pd.DataFrame(sheet3_od)

    excel_file_name = str(net_name) + '.xlsx'
    writer = ExcelWriter(excel_file_name)
    sheet1_df.to_excel(writer, 'Sheet1', index=False)
    sheet2_df.to_excel(writer, 'Sheet2', index=False)
    sheet3_df.to_excel(writer, 'Sheet3', index=False)
    writer.save()

if __name__ == '__main__':
    extract_into_excel()
