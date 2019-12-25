#!/bin/bash

# densenet121 sparse int8
net=densenet121
prefix=${net}-sparse-int8
weight_path=/home/Cambricon-Test/Cambricon-MLU100/models/caffe/${net}
for sparsity in `seq 0.01 0.01 0.90`
do
log_file=mlu-${net}-int8-sparse-online-${sparsity}.log
caffe test -iterations 10 -mmode MLU -mludevice 0 -mcore MLU100 -model ${prefix}/${net}_float16_dense_1batch-int8-${sparsity}.prototxt.sparse -weights ${weight_path}/${net}_int8_sparse-${sparsity}.cnml.caffemodel 2>&1 | tee ${log_file}
rm -f test_mlu_iter*
done
