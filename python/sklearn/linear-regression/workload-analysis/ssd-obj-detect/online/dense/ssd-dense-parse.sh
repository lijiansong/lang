#!/bin/bash

#grep -rin "hardware time:" mlu-ssd_mobilenetv1-fp16-dense.log 2>&1 | tee time.log
#sed -i "s/layer input/layer data/" time.log
#python2 extract_ssd_dense_layer_time.py ssd_mobilenetv1_float16_dense_1batch-online.prototxt time.log
#python excel_io.py

#grep -rin "hardware time:" mlu-ssd_mobilenetv1-int8-dense.log 2>&1 | tee time.log
#sed -i "s/layer input/layer data/" time.log
#python2 extract_ssd_dense_layer_time.py ssd_mobilenetv1_float16_dense_1batch-int8-online.prototxt time.log
#python excel_io.py

#grep -rin "hardware time:" mlu-ssd_vgg16-fp16-dense.log 2>&1 | tee time.log
#sed -i "s/layer input/layer data/" time.log
#python2 extract_ssd_dense_layer_time.py ssd_vgg16_float16_dense_1batch-online.prototxt time.log
#python excel_io.py

#grep -rin "hardware time:" mlu-ssd_vgg16-int8-dense.log 2>&1 | tee time.log
#sed -i "s/layer input/layer data/" time.log
#python2 extract_ssd_dense_layer_time.py ssd_vgg16_float16_dense_1batch-int8-online.prototxt time.log
#python excel_io.py

net_list=(
"ssd_mobilenetv1"
"ssd_vgg16"
)
data_type=(
"fp16"
"int8"
)
for type in ${data_type[@]}; do
    for net in ${net_list[@]}; do
        echo "${net}, dense, ${type}"
        grep -rin "hardware time:" mlu-${net}-${type}-dense.log 2>&1 | tee time.log
        sed -i "s/layer input/layer data/" time.log
        if [ ${type} = "int8" ]; then
            python2 extract_ssd_dense_layer_time.py ${net}_float16_dense_1batch-int8-online.prototxt time.log
        else
            python2 extract_ssd_dense_layer_time.py ${net}_float16_dense_1batch-online.prototxt time.log
        fi
        python excel_io.py
    done
done

for net in ${net_list[@]}; do
    echo ${net}
    ls ${net}-dense-*.xlsx | wc -l
done
