#!/usr/bin/env python3

import sys
import re
import os
import collections
import pickle

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

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

    flops_membwd_reader = open(str(net_name) + '-flops_membwd.txt', 'rb')
    flops_membwd_dict = pickle.load(flops_membwd_reader)

    layer_name_list = []
    layer_name_type_list = []
    layer_name_time_list = []
    layer_type_list = []
    layer_type_time_list = []
    flops_membwd_type_list = []
    flops_membwd_values_list = []

    max_bottoms_length = max_tops_length = 0
    # multiple input and output shape info
    layer_shape_list_dict = {}
    kernel_size_list = []
    stride_list = []
    pad_list = []

    try:
        for k, v in list(layer_shape.items()):
            if v['type'] == 'Input' or v['type'] == 'Accuracy':
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

        for k, v in flops_membwd_dict.items():
            flops_membwd_type_list.append(str(k))
            flops_membwd_values_list.append(float(v))

    finally:
        layer_info_reader.close()
        layer_shape_reader.close()
        layer_name_time_reader.close()
        layer_type_time_reader.close()
        flops_membwd_reader.close()

    assert len(layer_name_list) == len(layer_name_time_list) and \
            len(layer_name_time_list) == len(kernel_size_list) and \
            len(kernel_size_list) == len(stride_list) and \
            len(stride_list) == len(pad_list) and \
            len(layer_type_list) == len(layer_type_time_list) and \
            len(flops_membwd_type_list) == len(flops_membwd_values_list), \
            " Error! Must have same records length!"

    sheet1_od = collections.OrderedDict()
    sheet1_od['layer name'] = layer_name_list
    sheet1_od['layer type'] = layer_name_type_list
    sheet1_od['time(ms)'] = layer_name_time_list
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
    sheet3_od['type'] = flops_membwd_type_list
    sheet3_od['values'] = flops_membwd_values_list
    sheet3_df = pd.DataFrame(sheet3_od)

    excel_file_name = str(net_name) + '.xlsx'
    writer = ExcelWriter(excel_file_name)
    sheet1_df.to_excel(writer, 'Sheet1', index=False)
    sheet2_df.to_excel(writer, 'Sheet2', index=False)
    sheet3_df.to_excel(writer, 'Sheet3', index=False)
    writer.save()

if __name__ == '__main__':
    extract_into_excel()
