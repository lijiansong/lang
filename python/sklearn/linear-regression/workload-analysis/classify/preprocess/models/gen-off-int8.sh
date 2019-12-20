#!/bin/bash
exe=caffe
net=densenet121
for sparsity in `seq 0.10 0.10 0.90`
do
batch=1
mp=1
model_file=${net}_float16_dense_1batch-int8-${sparsity}.prototxt.sparse
weight_file=${net}_int8_sparse-${sparsity}.cnml.caffemodel
${exe} genoff -model ${model_file} -weights ${weight_file} -mcore MLU100 -model_parallel ${mp}
mv offline.cambricon offline-${net}-int8-sparse-${sparsity}-${batch}batch-${mp}.cambricon
done
