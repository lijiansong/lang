#!/bin/bash
# --------------------------------------------------------
# Extract final accuracy.
# classification, imagenet ILSVRC2012 5w images,
# object detection, VOC2012 1w images.
# --------------------------------------------------------

current_dir=`pwd`
exe=${current_dir}/../../build/examples/clas_offline_multicore/clas_offline_multicore

# final acc logs

# ------------------------
# densenet121 dense int8
#net=densenet121
#batch=1
#dp=4
#mp=1
#tn=8
#${exe} -offlinemodel ${current_dir}/offline-${net}-int8/offline-${net}-int8-dense-${batch}batch-${mp}.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${current_dir}/${net}.log-int8-dense-${batch}batch-${dp}-${mp}-${tn}
# ------------------------
# densenet121 dense fp16
#net=densenet121
#batch=1
#dp=4
#mp=1
#tn=8
#offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/densenet121/offline-densenet121-fp16-dense-1batch-1.cambricon
#${exe} -offlinemodel ${offline_model_file} -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${current_dir}/${net}.log-fp16-dense-${batch}batch-${dp}-${mp}-${tn}
# ------------------------

net=densenet121
batch=1
dp=4
mp=1
tn=8
for round in `seq 1 3`
do
for sparsity in `seq 0.01 0.01 0.80`
do
echo "net: ${net}, sparsity: ${sparsity}, batch: ${batch}, dp: ${dp}, mp: ${mp}, tn: ${tn}"
offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/${net}/offline-${net}-fp16-sparse-${sparsity}-1batch-1.cambricon
log_file=${net}.log-fp16-sparse-${sparsity}-${batch}batch-${dp}-${mp}-${tn}-round-${round}
${exe} -offlinemodel ${offline_model_file} -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${log_file}
done
done

#net=densenet121
#batch=1
#dp=4
#mp=1
#tn=8
#for sparsity in `seq 0.10 0.10 0.90`
#do
#echo "net: ${net}, sparsity: ${sparsity}, batch: ${batch}, dp: ${dp}, mp: ${mp}, tn: ${tn}"
#offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/${net}/offline-${net}-int8-sparse-${sparsity}-1batch-1.cambricon
#${exe} -int8 1 -offlinemodel ${offline_model_file} -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${current_dir}/${net}.log-int8-sparse-${sparsity}-${batch}batch-${dp}-${mp}-${tn}
#done
