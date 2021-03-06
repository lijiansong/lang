#!/bin/bash
# --------------------------------------------------------
# Extract final accuracy.
# classification, imagenet ILSVRC2012 5w images,
# object detection, VOC2012 1w images.
# --------------------------------------------------------

current_dir=`pwd`
exe=${current_dir}/../../build/examples/ssd/ssd_offline_multicore
VOC_PATH=../../../../../datasets/VOC2012/Annotations

# ssd_vgg16 sparse fp16
network=ssd_vgg16
for round in `seq 1 3`
do
for sparsity in `seq 0.01 0.01 0.70`
do
batch=1
dp=1
mp=1
tn=32
echo "network: ${network}, sparsity: ${sparsity}, batch: ${batch}, dp: ${dp}, mp: ${mp}"
model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/${network}/offline-${network}-fp16-sparse-${sparsity}-1batch-1.cambricon
log_file=${network}.log-fp16-sparse-${sparsity}-${batch}batch-${dp}-${mp}-${tn}-round-${round}
${exe} -offlinemodel ${model_file} -images val.txt -labelmapfile labelmap_voc.prototxt -confidencethreshold 0.6 -Bangop 0 -dump 1 -threads ${tn} -dataparallel ${dp} &>> ${log_file}
python ../../scripts/meanAP_VOC.py val.txt ${current_dir}/ ${VOC_PATH} &>> ${log_file}
rm 2007*.txt 2008*.txt 2009*.txt 2010*.txt 2011*.txt 2012*.txt ssd_*.jpg
done
done
