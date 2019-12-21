#!/bin/bash

PREFIX=ssd_mobilenetv1-int8-sparse
for sparsity in `seq 0.20 0.10 0.90`;
do
    pushd .
    cd ${PREFIX}-${sparsity}
    ./extract.sh
    cd scripts
    ./run.sh
    popd
done

