#!/bin/bash
set -e

network_list=(
      #alexnet
      #googlenet
      #inception-v3
      #mobilenet
      #resnet101
      #resnet152
      #resnet18
      #resnet34
      #resnet50
      #squeezenet
      #vgg16
      #vgg19
      #densenet121
      #densenet161
      #densenet169
      #densenet201
      #mobilenet-github
      #mobilenet_v2-github
      ssd_mobilenetv1
      ssd_vgg16
      faster-rcnn
)
for net in ${network_list[@]}; do
echo "===----- ${net} -----==="
pushd .
cd ${net}
for i in `seq 0.10 0.01 0.90`;
do
    echo "===--- ${i} ---==="
    set_sparse ${net}_float16_dense_1batch.prototxt ${i}
    mv ${net}_float16_dense_1batch.prototxt.sparse ${net}_float16_dense_1batch-${i}.prototxt.sparse
    convert_caffemodel.bin proto -model ${net}_float16_dense_1batch-${i}.prototxt.sparse -weights ${net}_float16_dense.caffemodel
    # we will get final.cnml.caffemodel
    # save prototxt and weights
    if [ ! -d sparse-${i} ];then
        mkdir sparse-${i}
    fi
    mv ${net}_float16_dense.cnml.caffemodel ${net}_float16_dense_1batch-${i}.prototxt.sparse sparse-${i}
done
popd
done
