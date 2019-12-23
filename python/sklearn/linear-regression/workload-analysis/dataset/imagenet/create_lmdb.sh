#!/bin/bash
DATA_PATH=/home/Cambricon-Test/Cambricon-MLU100/datasets/imagenet/
DB_PATH=imagenet_ILSVRC2012_lmdb-256
if [ -d ${DB_PATH} ];
then
    rm -rf ${DB_PATH}
fi
#convert_imageset --shuffle \
#    --resize_height=224 --resize_width=224 \
#    ${DATA_PATH} ./val.txt ${DB_PATH}
convert_imageset --shuffle \
    --resize_height=256 --resize_width=256 \
    ${DATA_PATH} ./val.txt ${DB_PATH}
