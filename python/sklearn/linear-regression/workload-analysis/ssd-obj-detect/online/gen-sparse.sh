#!/bin/bash
net=ssd_mobilenetv1
model_file=${net}_float16_dense_1batch.prototxt
weight_file=${net}_float16_dense.caffemodel

for sparsity in `seq 0.01 0.01 0.90`
do
# 1. generate the sparse model file
set_sparse ${model_file} ${sparsity}

out_sparse_model_file=${net}_float16_dense_1batch-${sparsity}.prototxt.sparse
mv ${net}_float16_dense_1batch.prototxt.sparse ${out_sparse_model_file}

sed -i "30s/sparse_mode: true/\#sparse_mode: true/" ${out_sparse_model_file}
convert_caffemodel.bin proto -model ${out_sparse_model_file} -weights ${weight_file}

out_sparse_weight_file=${net}_float16_dense-${sparsity}.cnml.caffemodel
mv ${net}_float16_dense.cnml.caffemodel ${out_sparse_weight_file}

# 2. execute at mlu100

log_file=mlu-${net}-fp16-sparse-online-${sparsity}.log
caffe test -iterations 5 -mmode MLU -mludevice 0 -mcore MLU100 -weights ${out_sparse_weight_file} -model ${out_sparse_model_file} 2>&1 | tee ${log_file}
rm -f ${out_sparse_weight_file} ${out_sparse_model_file}
done
