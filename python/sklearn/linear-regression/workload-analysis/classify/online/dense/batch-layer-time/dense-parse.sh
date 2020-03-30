#!/bin/bash
set -e
#grep -rin "time:" mlu100-mobilenet-1batch-fp16.log 2>&1 | tee time.log
#python2 extract_dense_layer_time.py ../mobilenet_float16_dense_1batch-online.prototxt time.log mobilenet 1
#python excel_io.py
#
#grep -rin "time:" mlu100-squeezenet-1batch-fp16.log 2>&1 | tee time.log
#python2 extract_dense_layer_time.py ../squeezenet_float16_dense_1batch-online.prototxt time.log squeezenet 1
#python excel_io.py
#
grep -rin "time:" mlu100-resnet50-1batch-fp16.log 2>&1 | tee time.log
python2 extract_dense_layer_time.py ../resnet50_float16_dense_1batch-online.prototxt time.log resnet50 1
python excel_io.py
#
#grep -rin "time:" mlu100-densenet121-1batch-fp16.log 2>&1 | tee time.log
#python2 extract_dense_layer_time.py ../densenet121_float16_dense_1batch-online.prototxt time.log densenet121 1
#python excel_io.py

#batch_list=(
#1
#2
#4
#8
#16
#32
#64
#)
#batch_size_lineno_map=(
#"mobilenet|19"
#"squeezenet|16"
#"densenet121|22"
#"resnet50|21"
#)
#
#for batch in ${batch_list[@]}; do
#    for item in ${batch_size_lineno_map[@]}; do
#        net=$(echo "${item}"|awk -F "|" '{print $1}')
#        line_no=$(echo "${item}"|awk -F "|" '{print $2}')
#        echo "${net}, dense, fp16"
#        net_file=../${net}_float16_dense_1batch-online.prototxt
#        log_file=mlu100-${net}-${batch}batch-fp16.log
#        if [ -f ${log_file} ]; then
#            grep -rin "time:" ${log_file} 2>&1 | tee time.log
#            sed -i "${line_no}s/batch_size:\ [0-9]*/batch_size:\ ${batch}/" ${net_file}
#            python2 extract_dense_layer_time.py ${net_file} time.log ${net} ${batch}
#            python excel_io.py
#        fi
#    done
#done
#
#net_list=(
#mobilenet
#squeezenet
#densenet121
#resnet50
#)
#
#for net in ${net_list[@]}; do
#    echo ${net}
#    ls ${net}-*.xlsx | wc -l
#done
