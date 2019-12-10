#!/bin/bash
# -----------------------------------------
# Offline run for sparse float16.
# -----------------------------------------
current_dir=`pwd`
exe=${current_dir}/../../build/examples/clas_offline_multicore/clas_offline_multicore

batchsize_list=(
     1
     2
     4
     8
     16
     32
    # 64
)

threads_list=(
     1
     2
     4
     8
     16
     32
     #64
)

dpmp_list1=(
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
dpmp_list2=(
    '16 1'
    '16 2'
    '32 1'
)
dpmp_list3=(
    '1 16'
    '1 32'
    '2 16'
)

network_list=(
    #alexnet
    #resnet50
    #squeezenet
    densenet121
    mobilenet
    #googlenet
    #inception-v3
    #vgg16
    #vgg19
    #mobilenet-github
    #mobilenet_v2-github
)

echo -e "\n===================================================="

for round in `seq 1 5`; do
for net in ${network_list[@]}; do
for sparse in `seq 0.10 0.10 0.90`; do
for batch in "${batchsize_list[@]}"; do
    for dpmp in "${dpmp_list1[@]}"; do
        # dp: data parallel; mp: model parallel
        dp=${dpmp:0:1}
        mp=${dpmp:2:1}
        for thread_num in "${threads_list[@]}"; do
            echo "net: $net, sparsity: ${sparse}, dataparallel:  $dp,  modelparallel:  $mp, batch size: $batch, threads: ${thread_num}, round: ${round}"
            offline_model_file=${current_dir}/offline-${net}-int8-sparse/sparse-${sparse}/offline-${net}-int8-sparse-${sparse}-${batch}batch-${mp}.cambricon
            if [ -f ${offline_model_file} ]
            then
                ${exe} -offlinemodel ${offline_model_file} -images ${current_dir}/val-2k.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads ${thread_num} -dataparallel ${dp} &>> ${current_dir}/${net}.log-int8-sparse-${sparse}-${batch}batch-${dp}-${mp}-${thread_num}-round-${round}
            fi
        done
    done
    for dpmp in "${dpmp_list2[@]}"; do
        # dp: data parallel; mp: model parallel
        dp=${dpmp:0:2}
        mp=${dpmp:3:1}
        for thread_num in "${threads_list[@]}"; do
            echo "net: $net, sparsity: ${sparse}, dataparallel:  $dp,  modelparallel:  $mp, batch size: $batch, threads: ${thread_num}, round: ${round}"
            offline_model_file=${current_dir}/offline-${net}-int8-sparse/sparse-${sparse}/offline-${net}-int8-sparse-${sparse}-${batch}batch-${mp}.cambricon
            if [ -f ${offline_model_file} ]
            then
                ${exe} -offlinemodel ${offline_model_file} -images ${current_dir}/val-2k.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads ${thread_num} -dataparallel ${dp} &>> ${current_dir}/${net}.log-int8-sparse-${sparse}-${batch}batch-${dp}-${mp}-${thread_num}-round-${round}
            fi
        done
    done
    for dpmp in "${dpmp_list3[@]}"; do
        # dp: data parallel; mp: model parallel
        dp=${dpmp:0:1}
        mp=${dpmp:2:2}
        for thread_num in "${threads_list[@]}"; do
            echo "net: $net, sparsity: ${sparse}, dataparallel:  $dp,  modelparallel:  $mp, batch size: $batch, threads: ${thread_num}, round: ${round}"
            offline_model_file=${current_dir}/offline-${net}-int8-sparse/sparse-${sparse}/offline-${net}-int8-sparse-${sparse}-${batch}batch-${mp}.cambricon
            if [ -f ${offline_model_file} ]
            then
                ${exe} -offlinemodel ${offline_model_file} -images ${current_dir}/val-2k.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads ${thread_num} -dataparallel ${dp} &>> ${current_dir}/${net}.log-int8-sparse-${sparse}-${batch}batch-${dp}-${mp}-${thread_num}-round-${round}
            fi
        done
    done
done
done
done
done
