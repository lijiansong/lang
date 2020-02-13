#!/bin/bash
#grep -rin "time:" mlu-mobilenet-int8-sparse-online-0.87.log 2>&1 | tee time.log
#python2 extract_layer_time.py mobilenet-sparse-int8/mobilenet_float16_dense_1batch-int8-0.87.prototxt.sparse time.log
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
        for sparsity in `seq 0.01 0.01 0.90`; do
            echo "${net}, ${type}, sparse, ${sparsity}"
            grep -rin "time:" mlu-${net}-${type}-sparse-online-${sparsity}.log 2>&1 | tee time.log
            if [ ${type} = "int8" ]; then
                python2 extract_layer_time.py ${net}-sparse-int8/${net}_float16_dense_1batch-int8-${sparsity}.prototxt.sparse time.log
            else
                python2 extract_layer_time.py ${net}-sparse-fp16/${net}_float16_dense_1batch-${sparsity}.prototxt.sparse time.log
            fi
            python excel_io.py
        done
    done
done

for net in ${net_list[@]}; do
    echo ${net}
    ls ${net}-sparse-*.xlsx | wc -l
done
