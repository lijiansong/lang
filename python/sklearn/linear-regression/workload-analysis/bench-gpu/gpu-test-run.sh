#!/bin/bash

network_list=(
densenet121
mobilenet
resnet50
squeezenet
)

batch_list=(
1
2
4
8
16
32
64
)
batchsize_lineno_map=(
"mobilenet|30"
"squeezenet|36"
"densenet121|27"
"resnet50|30"
)
for net_item in ${batchsize_lineno_map[@]}; do
    net=$(echo "${net_item}"|awk -F "|" '{print $1}')
    line_no=$(echo "${net_item}"|awk -F "|" '{print $2}')
    net_file=${net}/${net}-online.prototxt
    weight_file=${net}/${net}_float16_dense.caffemodel
    for batch in ${batch_list[@]}; do
        sed -i "${line_no}s/batch_size:\ [0-9]*/batch_size:\ ${batch}/" ${net_file}
        log_file=gpu-${net}-${batch}batch-fp32.log
        echo "${net}, ${batch} batch"
        caffe time -model ${net_file} -weights ${weight_file} -gpu 0 -iterations 10 2>&1 | tee ${log_file}
    done
done
