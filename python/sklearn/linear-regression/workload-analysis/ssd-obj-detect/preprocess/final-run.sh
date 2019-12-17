#!/bin/bash

current_dir=`pwd`
exe=${current_dir}/../../build/examples/ssd/ssd_offline_multicore
VOC_PATH=../../../../../datasets/VOC2012/Annotations

# Note: the crash point file is ssd_mobilenetv1.log-fp16-dense-16batch-2-2-64-round-1
network=ssd_mobilenetv1
# --------------------------
batch=16
dp=2
mp=2
thread_num=64
echo "network: ${network}, batch: ${batch}, dp: ${dp}, mp: ${mp}"
model_file=${current_dir}/offline-${network}/offline-${network}-dense-fp16-${batch}batch-${mp}.cambricon
${exe} -offlinemodel ${model_file} -images file_list_for_release -labelmapfile labelmap_voc.prototxt -confidencethreshold 0.6 -Bangop 0 -dump 1 -threads ${thread_num} -dataparallel ${dp}
python ../../scripts/meanAP_VOC.py file_list_for_release ${current_dir}/ ${VOC_PATH}
rm 2007*.txt 2008*.txt ssd_*.jpg
# --------------------------
batch=32
dp=1
mp=1
thread_num=1
echo "network: ${network}, batch: ${batch}, dp: ${dp}, mp: ${mp}"
model_file=${current_dir}/offline-${network}/offline-${network}-dense-fp16-${batch}batch-${mp}.cambricon
${exe} -offlinemodel ${model_file} -images file_list_for_release -labelmapfile labelmap_voc.prototxt -confidencethreshold 0.6 -Bangop 0 -dump 1 -threads ${thread_num} -dataparallel ${dp}
python ../../scripts/meanAP_VOC.py file_list_for_release ${current_dir}/ ${VOC_PATH}
rm 2007*.txt 2008*.txt ssd_*.jpg
# --------------------------
batch=16
dp=2
mp=2
thread_num=32
echo "network: ${network}, batch: ${batch}, dp: ${dp}, mp: ${mp}"
${exe} -offlinemodel ${model_file} -images file_list_for_release -labelmapfile labelmap_voc.prototxt -confidencethreshold 0.6 -Bangop 0 -dump 1 -threads ${thread_num} -dataparallel ${dp}
python ../../scripts/meanAP_VOC.py file_list_for_release ${current_dir}/ ${VOC_PATH}
rm 2007*.txt 2008*.txt ssd_*.jpg
# --------------------------
