#!/bin/bash

#grep -rin "hardware time:" mlu100-ssd_mobilenetv1-1batch-fp16.log 2>&1 | tee time.log
#sed -i "s/layer input/layer data/" time.log
#python2 extract_ssd_dense_layer_time.py ../ssd_mobilenetv1_float16_dense_1batch-online.prototxt time.log ssd_mobilenetv1 1
#python excel_io.py
#
#grep -rin "hardware time:" mlu100-ssd_vgg16-1batch-fp16.log 2>&1 | tee time.log
#sed -i "s/layer input/layer data/" time.log
#python2 extract_ssd_dense_layer_time.py ../ssd_vgg16_float16_dense_1batch-online.prototxt time.log ssd_vgg16 1
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
#"ssd_mobilenetv1|15"
"ssd_vgg16|8"
)

for batch in ${batch_list[@]}; do
    for item in ${batch_size_lineno_map[@]}; do
        net=$(echo "${item}"|awk -F "|" '{print $1}')
        line_no=$(echo "${item}"|awk -F "|" '{print $2}')
        echo "${net}, dense, fp16"
        net_file=../${net}_float16_dense_1batch-online.prototxt
        log_file=mlu100-${net}-${batch}batch-fp16.log
        if [ -f ${log_file} ]; then
            grep -rin "hardware time:" ${log_file} 2>&1 | tee time.log
            sed -i "${line_no}s/dim:\ [0-9]*/dim:\ ${batch}/" ${net_file}
            sed -i "s/layer input/layer data/" time.log
            python2 extract_ssd_dense_layer_time.py ${net_file} time.log ${net} ${batch}
            python excel_io.py
        fi
    done
done

net_list=(
ssd_mobilenetv1
ssd_vgg16
)

for net in ${net_list[@]}; do
    echo ${net}
    ls ${net}-*.xlsx | wc -l
done
