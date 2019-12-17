#!/bin/bash

current_dir=`pwd`
exe=${current_dir}/../../build/examples/ssd/ssd_offline_multicore

batch_size_list=(
1
2
4
8
16
32
#64
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
dp_mp_list2=(
    '16 1'
    '16 2'
    '32 1'
)

network_list=(
ssd_mobilenetv1
#faster-rcnn
)

VOC_PATH=../../../../../datasets/VOC2012/Annotations
for round in `seq 2 5`; do
for network in "${network_list[@]}"; do
    for batch in "${batch_size_list[@]}"; do
    for thread_num in "${thread_num_list[@]}"; do
    for dpmp in "${dp_mp_list0[@]}"; do
        dp=${dpmp:0:1}
        mp=${dpmp:2:1}
        echo "net: ${network}, batch: ${batch}, data parallelism: ${dp}, model parallelism: ${mp}, thread num: ${thread_num}, round: ${round}"
        model_file=${current_dir}/offline-${network}/offline-${network}-dense-fp16-${batch}batch-${mp}.cambricon
        log_file=${network}.log-fp16-dense-${batch}batch-${dp}-${mp}-${thread_num}-round-${round}
        if [ -f ${model_file} ]
        then
            ${exe} -offlinemodel ${model_file} -images file_list_for_release -labelmapfile labelmap_voc.prototxt -confidencethreshold 0.6 -Bangop 0 -dump 1 -threads ${thread_num} -dataparallel ${dp} &>>${log_file}
            python ../../scripts/meanAP_VOC.py file_list_for_release ${current_dir}/ ${VOC_PATH} &>>${log_file}
            rm 2007*.txt 2008*.txt *.jpg >/dev/null
        fi
    done
    for dpmp in "${dp_mp_list1[@]}"; do
        dp=${dpmp:0:1}
        mp=${dpmp:2:2}
        echo "net: ${network}, batch: ${batch}, data parallelism: ${dp}, model parallelism: ${mp}, thread num: ${thread_num}, round: ${round}"
        model_file=${current_dir}/offline-${network}/offline-${network}-dense-fp16-${batch}batch-${mp}.cambricon
        log_file=${network}.log-fp16-dense-${batch}batch-${dp}-${mp}-${thread_num}-round-${round}
        if [ -f ${model_file} ]
        then
            ${exe} -offlinemodel ${model_file} -images file_list_for_release -labelmapfile labelmap_voc.prototxt -confidencethreshold 0.6 -Bangop 0 -dump 1 -threads ${thread_num} -dataparallel ${dp} &>>${log_file}
            python ../../scripts/meanAP_VOC.py file_list_for_release ${current_dir}/ ${VOC_PATH} &>>${log_file}
            rm 2007*.txt 2008*.txt *.jpg >/dev/null
        fi
    done
    for dpmp in "${dp_mp_list2[@]}"; do
        dp=${dpmp:0:2}
        mp=${dpmp:3:1}
        echo "net: ${network}, batch: ${batch}, data parallelism: ${dp}, model parallelism: ${mp}, thread num: ${thread_num}, round: ${round}"
        model_file=${current_dir}/offline-${network}/offline-${network}-dense-fp16-${batch}batch-${mp}.cambricon
        log_file=${network}.log-fp16-dense-${batch}batch-${dp}-${mp}-${thread_num}-round-${round}
        if [ -f ${model_file} ]
        then
            ${exe} -offlinemodel ${model_file} -images file_list_for_release -labelmapfile labelmap_voc.prototxt -confidencethreshold 0.6 -Bangop 0 -dump 1 -threads ${thread_num} -dataparallel ${dp} &>>${log_file}
            python ../../scripts/meanAP_VOC.py file_list_for_release ${current_dir}/ ${VOC_PATH} &>>${log_file}
            rm 2007*.txt 2008*.txt *.jpg >/dev/null
        fi
    done
    done
done
done
done
