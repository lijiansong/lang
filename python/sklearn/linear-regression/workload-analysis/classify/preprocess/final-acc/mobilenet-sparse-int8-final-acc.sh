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
# mobilenet dense int8
#net=mobilenet
#batch=1
#dp=4
#mp=1
#tn=8
#${exe} -offlinemodel ${current_dir}/offline-${net}-int8/offline-${net}-int8-dense-${batch}batch-${mp}.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${current_dir}/${net}.log-int8-dense-${batch}batch-${dp}-${mp}-${tn}
# ------------------------
# mobilenet dense fp16
#net=mobilenet
#batch=1
#dp=4
#mp=1
#tn=8
#${exe} -offlinemodel ${current_dir}/offline-${net}/offline-${net}-float16-dense-${batch}batch-${mp}.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${current_dir}/${net}.log-fp16-dense-${batch}batch-${dp}-${mp}-${tn}
# ------------------------
# mobilenet sparse fp16 0.10
#net=mobilenet
#batch=1
#dp=4
#mp=1
#tn=4
#sparsity=0.10
#offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/mobilenet/offline-mobilenet-fp16-sparse-${sparsity}-1batch-1.cambricon
#${exe} -offlinemodel ${offline_model_file} -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} #&>> ${current_dir}/${net}.log-fp16-sparse-${sparsity}-${batch}batch-${dp}-${mp}-${tn}
# ------------------------

#net=mobilenet
#batch=1
#dp=4
#mp=1
#tn=16
#for round in `seq 1 5`
#do
#for sparsity in `seq 0.10 0.10 0.90`
#do
#echo "net: ${net}, sparsity: ${sparsity}, batch: ${batch}, dp: ${dp}, mp: ${mp}, tn: ${tn}"
#offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/mobilenet/offline-mobilenet-fp16-sparse-${sparsity}-1batch-1.cambricon
#log_file=${net}.log-fp16-sparse-${sparsity}-${batch}batch-${dp}-${mp}-${tn}-round-${round}
#${exe} -offlinemodel ${offline_model_file} -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${log_file}
#done
#done

# ------------------------
# mobilenet sparse int8 0.10
#net=mobilenet
#batch=1
#dp=4
#mp=1
#tn=4
#sparsity=0.10
##offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/mobilenet/offline-mobilenet-fp16-sparse-${sparsity}-1batch-1.cambricon
##offline_model_file=offline-${net}-int8-sparse/sparse-${sparsity}/offline-${net}-int8-sparse-${sparsity}-${batch}batch-${mp}.cambricon
#offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/mobilenet/offline.cambricon
#${exe} -int8 1 -offlinemodel ${offline_model_file} -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} #&>> ${current_dir}/${net}.log-fp16-sparse-${sparsity}-${batch}batch-${dp}-${mp}-${tn}
# ------------------------

net=mobilenet
batch=1
dp=4
mp=1
tn=16
for round in `seq 1 3`
do
for sparsity in `seq 0.01 0.01 0.70`
do
echo "net: ${net}, sparsity: ${sparsity}, batch: ${batch}, dp: ${dp}, mp: ${mp}, tn: ${tn}"
offline_model_file=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/mobilenet/offline-mobilenet-int8-sparse-${sparsity}-1batch-1.cambricon
log_file=${net}.log-int8-sparse-${sparsity}-${batch}batch-${dp}-${mp}-${tn}-round-${round}
${exe} -int8 1 -offlinemodel ${offline_model_file} -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -fifosize 2  -threads ${tn} -dataparallel ${dp} &>> ${log_file}
done
done

