#!/bin/bash
#grep -rin "time:" mlu-mobilenet-fp16-dense.log 2>&1 | tee time.log
#python2 extract_dense_layer_time.py mobilenet_float16_dense_1batch-online.prototxt time.log
#python excel_io.py

#grep -rin "time:" mlu-squeezenet-fp16-dense.log 2>&1 | tee time.log
#python2 extract_dense_layer_time.py squeezenet_float16_dense_1batch-online.prototxt time.log
#python excel_io.py

#grep -rin "time:" mlu-resnet50-fp16-dense.log 2>&1 | tee time.log
#python2 extract_dense_layer_time.py resnet50_float16_dense_1batch-online.prototxt time.log
#python excel_io.py

net_list=(
"mobilenet"
"squeezenet"
"densenet121"
"resnet50"
)
data_type=(
"fp16"
"int8"
)
for type in ${data_type[@]}; do
    for net in ${net_list[@]}; do
        echo "${net}, dense, ${type}"
        grep -rin "time:" mlu-${net}-${type}-dense.log 2>&1 | tee time.log
        if [ ${type} = "int8" ]; then
            python2 extract_dense_layer_time.py ${net}_float16_dense_1batch-int8-online.prototxt time.log
        else
            python2 extract_dense_layer_time.py ${net}_float16_dense_1batch-online.prototxt time.log
        fi
        python excel_io.py
    done
done

for net in ${net_list[@]}; do
    echo ${net}
    ls ${net}-dense-*.xlsx | wc -l
done
