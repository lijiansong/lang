#!/usr/bin/env python3

import sys
import re
import os
import collections
import pickle

import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

def extract_into_excel(layer_info='layer_info.txt'):
    layer_info_reader = open(layer_info, 'rb')
    layer_info = pickle.load(layer_info_reader)
    net_name = layer_info['name']
    print(net_name)
    layer_name_time_reader = open(str(net_name) + '-each_layer_time.txt', 'rb')
    layer_type_time_reader = open(str(net_name) + '-layer_type_time.txt', 'rb')

    layer_name_record_dict = pickle.load(layer_name_time_reader)
    layer_type_record_dict = pickle.load(layer_type_time_reader)

    layer_name_list = []
    layer_name_type_list = []
    layer_name_time_list = []
    layer_type_list = []
    layer_type_time_list = []

    try:
        for k, v in layer_name_record_dict.items():
            layer_name_list.append(str(k))
            layer_name_type_list.append(str(layer_info[str(k)]))
            layer_name_time_list.append(float(v))

        for k, v in layer_type_record_dict.items():
            layer_type_list.append(str(k))
            layer_type_time_list.append(float(v))
    finally:
        layer_info_reader.close()
        layer_name_time_reader.close()
        layer_type_time_reader.close()

    assert len(layer_name_list) == len(layer_name_time_list) and \
            len(layer_type_list) == len(layer_type_time_list), \
            " Error! Must have same records length!"

    sheet1_od = collections.OrderedDict()
    sheet1_od['layer name'] = layer_name_list
    sheet1_od['layer type'] = layer_name_type_list
    sheet1_od['time(ms)'] = layer_name_time_list
    sheet1_df = pd.DataFrame(sheet1_od)

    sheet2_od = collections.OrderedDict()
    sheet2_od['layer type'] = layer_type_list
    sheet2_od['time(ms)'] = layer_type_time_list
    sheet2_df = pd.DataFrame(sheet2_od)
    excel_file_name = str(net_name) + '.xlsx'
    writer = ExcelWriter(excel_file_name)
    sheet1_df.to_excel(writer, 'Sheet1', index=False)
    sheet2_df.to_excel(writer, 'Sheet2', index=False)
    writer.save()

if __name__ == '__main__':
    extract_into_excel()
