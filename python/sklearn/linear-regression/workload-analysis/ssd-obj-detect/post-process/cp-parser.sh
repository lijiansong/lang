#!/bin/bash

PREFIX=ssd_mobilenetv1-fp16-sparse
for sparsity in `seq 0.20 0.10 0.90`;
do
    cp -r ${PREFIX}-0.10/*.sh ${PREFIX}-${sparsity}
    cp -r ${PREFIX}-0.10/*.py ${PREFIX}-${sparsity}
    cp -r ${PREFIX}-0.10/scripts ${PREFIX}-${sparsity}
done

