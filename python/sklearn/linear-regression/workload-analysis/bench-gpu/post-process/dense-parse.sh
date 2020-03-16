#!/bin/bash

#grep -rin "forward:" gpu-mobilenet-1batch-fp32.log 2>&1 | tee time.log
#sed -i "s/input/data/" time.log
#grep -rin "Average Forward pass" gpu-mobilenet-1batch-fp32.log 2>&1 | tee forward.log
#python2 extract_layer_time.py mobilenet_float16_dense_1batch-online.prototxt time.log 1
#python excel_io.py
#
#grep -rin "forward:" gpu-ssd_mobilenetv1-1batch-fp32.log 2>&1 | tee time.log
#sed -i "s/input/data/" time.log
#grep -rin "Average Forward pass" gpu-mobilenet-1batch-fp32.log 2>&1 | tee forward.log
#python2 extract_layer_time.py ssd_mobilenetv1_float16_dense_1batch-online.prototxt time.log 1
#python excel_io.py

batch_list=(
1
2
4
8
16
32
64
)
batch_size_lineno_map=(
"mobilenet|8"
"squeezenet|8"
"densenet121|8"
"resnet50|8"
"ssd_mobilenetv1|8"
"ssd_vgg16|8"
)

for batch in ${batch_list[@]}; do
    for item in ${batch_size_lineno_map[@]}; do
        net=$(echo "${item}"|awk -F "|" '{print $1}')
        line_no=$(echo "${item}"|awk -F "|" '{print $2}')
        echo "${net}, dense, fp32"
        net_file=${net}_float16_dense_1batch-online.prototxt
        log_file=gpu-${net}-${batch}batch-fp32.log
        if [ -f ${log_file} ]; then
            sed -i "${line_no}s/dim:\ [0-9]*/dim:\ ${batch}/" ${net_file}
            grep -rin "forward:" gpu-${net}-${batch}batch-fp32.log 2>&1 | tee time.log
            sed -i "s/input/data/" time.log
            grep -rin "Average Forward pass" gpu-${net}-${batch}batch-fp32.log 2>&1 | tee forward.log
            python2 extract_layer_time.py ${net}_float16_dense_1batch-online.prototxt time.log ${batch}
            python excel_io.py
        fi
    done
done

net_list=(
mobilenet
squeezenet
densenet121
resnet50
ssd_mobilenetv1
ssd_vgg16
)
for net in ${net_list[@]}; do
    echo ${net}
    ls ${net}-*.xlsx | wc -l
done
