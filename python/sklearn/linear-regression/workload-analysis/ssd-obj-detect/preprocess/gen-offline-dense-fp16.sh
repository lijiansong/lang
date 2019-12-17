#!/bin/bash
# -----------------------------------------
# Generate offline models.
# -----------------------------------------

current_dir=`pwd`
exe=${current_dir}/../../build/tools/caffe

batch_size_list=(
1
2
4
8
16
32
64
#128
)

thread_num_list=(
1
2
4
8
16
32
64
)

dp_mp_list0=(
    '1 1'
    '1 2'
    '1 4'
    '1 8'
    '2 1'
    '2 2'
    '2 4'
    '2 8'
    '4 1'
    '4 2'
    '4 4'
    '4 8'
    '8 1'
    '8 2'
    '8 4'
)
dp_mp_list1=(
    '1 16'
    '1 32'
    '2 16'
)
dp_mp_list1=(
    '16 1'
    '16 2'
    '32 1'
)

mp_list=(
1
2
4
8
16
32
)

network_list=(
ssd_mobilenetv1
#faster-rcnn
)

path_prefix=/home/Cambricon-Test/Cambricon-MLU100/models/caffe
for network in "${network_list[@]}"; do
    proto_file=${path_prefix}/${network}/${network}_float16_dense_1batch.prototxt
    weight_file=${path_prefix}/${network}/${network}_float16_dense.caffemodel
    for batch in "${batch_size_list[@]}"; do
    sed -i "4s/dim: [0-9]*/dim: ${batch}/g" ${proto_file}
    for mp in "${mp_list[@]}";
    do
        echo "net: ${network}, model parallelism: ${mp}, batch: ${batch}"
        ${exe} genoff -model ${proto_file} -weights ${weight_file} -mcore MLU100 -Bangop 0  -model_parallel ${mp} &>> ${current_dir}/genoff-${network}_float16_dense_${batch}batch_${mp}.log
        mv offline.cambricon offline-${network}-dense-fp16-${batch}batch-${mp}.cambricon
    done
done
done
