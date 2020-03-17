#!/bin/bash
#python cc.py gpu-nvprof-mobilenet-1batch-fp32.log mobilenet 1
#python cc.py gpu-nvprof-ssd_mobilenetv1-1batch-fp32.log ssd_mobilenetv1 1

net_list=(
mobilenet
squeezenet
densenet121
resnet50
ssd_mobilenetv1
ssd_vgg16
)

batch_list=(
1
2
4
8
16
#32
#64
)

for batch in ${batch_list[@]}; do
    for net in ${net_list[@]}; do
        echo "${batch} ${net}"
        nvprof_log_file=gpu-nvprof-${net}-${batch}batch-fp32.log
        if [ -f ${nvprof_log_file} ]; then
            python cc.py ${nvprof_log_file} ${net} ${batch}
        fi
    done
done

for net in ${net_list[@]}; do
    echo ${net}
    ls nvprof-${net}*.xlsx | wc -l
done
