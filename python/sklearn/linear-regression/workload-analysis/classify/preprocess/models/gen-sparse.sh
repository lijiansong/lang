#!/bin/bash
net=densenet121
model_file=${net}_float16_dense_1batch.prototxt
weight_file=${net}_float16_dense.caffemodel

for sparsity in `seq 0.10 0.10 0.90`
do
set_sparse ${model_file} ${sparsity}

out_sparse_model_file=${net}_float16_dense_1batch-${sparsity}.prototxt.sparse
mv ${net}_float16_dense_1batch.prototxt.sparse ${out_sparse_model_file}

sed -i "23s/sparse_mode: true/\#sparse_mode: true/" ${out_sparse_model_file}
convert_caffemodel.bin proto -model ${out_sparse_model_file} -weights ${weight_file}

out_sparse_weight_file=${net}_float16_dense-${sparsity}.cnml.caffemodel
mv ${net}_float16_dense.cnml.caffemodel ${out_sparse_weight_file}
done
