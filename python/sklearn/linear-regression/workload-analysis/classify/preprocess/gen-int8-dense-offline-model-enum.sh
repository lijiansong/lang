#!/bin/bash
# -----------------------------------------
# Generate offline model.
# -----------------------------------------
current_dir=`pwd`

batchsize_list=(
     1
     2
     4
     8
     16
     32
     64
)
mp_list=(
1
2
4
8
16
32
)

batchsize_lineno_map=(
#"alexnet|4"
#"googlenet|4"
#"inception-v3|8"
"mobilenet|7"
#"resnet101|4"
#"resnet152|4"
#"resnet18|4"
#"resnet34|4"
"resnet50|7"
#"squeezenet|11"
#"vgg16|4"
#"vgg19|4"
"densenet121|7"
#"densenet161|4"
#"densenet169|4"
#"densenet201|4"
#"mobilenet-github|10"
#"mobilenet_v2-github|10"
)

echo -e "\n===================================================="
dir_prefix=/home/Cambricon-Test/Cambricon-MLU100/models/caffe

for item in ${batchsize_lineno_map[@]}; do
net=$(echo "${item}"|awk -F "|" '{print $1}')
line_no=$(echo "${item}"|awk -F "|" '{print $2}')
echo "${net}: ${line_no}"
model_file=${dir_prefix}/${net}/${net}_float16_dense_1batch-int8.prototxt
weight_file=${dir_prefix}/${net}/${net}_float16_dense.caffemodel
for batch in "${batchsize_list[@]}"; do
    sed -i "${line_no}s/dim:\ [0-9]*/dim:\ ${batch}/" ${model_file}
    for mp in "${mp_list[@]}"; do
        echo $mp
        # dp: data parallel; mp: model parallel
        caffe genoff -model ${model_file} -weights ${weight_file} -mcore MLU100  -model_parallel ${mp}
        mv offline.cambricon offline-${net}-int8-dense-${batch}batch-${mp}.cambricon
    done
done
done

# check each numbers
for item in ${batchsize_lineno_map[@]}; do
net=$(echo "${item}"|awk -F "|" '{print $1}')
echo "===------- ${net} ------==="
for batch in "${batchsize_list[@]}"; do
    # Note: we can use 'caffe genoff -batchsize' to specify batch size
    ls offline-${net}-int8-dense-${batch}batch-*.cambricon | wc -l
done
echo "===---------------------==="
done
