#!/bin/bash

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
"ssd_mobilenetv1|4"
"ssd_vgg16|4"
#"mobilenet|8"
#"squeezenet|11"
#"densenet121|4"
#"resnet50|4"
)
CAFFE=/home/ljs/work-space/ssd-caffe/build/tools/caffe
for net_item in ${batchsize_lineno_map[@]}; do
    net=$(echo "${net_item}"|awk -F "|" '{print $1}')
    line_no=$(echo "${net_item}"|awk -F "|" '{print $2}')
    net_file=${net}/${net}_float16_dense_1batch.prototxt
    for batch in ${batch_list[@]}; do
        sed -i "${line_no}s/dim:\ [0-9]*/dim:\ ${batch}/" ${net_file}
        log_file=gpu-${net}-${batch}batch-fp32.log
        echo "${net}, ${batch} batch"
        ${CAFFE} time -gpu 0 -model ${net_file} -iterations 10 2>&1 | tee ${log_file}
    done
done