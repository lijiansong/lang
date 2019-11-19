#!/bin/bash

declare line_map=(["100"]=1 ["200"]=2)
line_map["300"]="3"

echo ${line_map[@]}

# iterator
for key in ${!line_map[@]};
do
    echo ${key}
    echo ${line_map[${key}]}
done

network_list=(
     alexnet
     googlenet
     inception-v3
     mobilenet
     resnet101
     resnet152
     resnet18
     resnet34
     resnet50
     squeezenet
     vgg16
     vgg19
)
declare batchsize_lineno_map=(["alexnet"]=4 ["googlenet"]=4 ["inception-v3"]=8 ["mobilenet"]=8 ["resnet101"]=4 ["resnet152"]=4 ["resnet18"]=4 ["resnet34"]=4 ["resnet50"]=4 ["squeezenet"]=11 ["vgg16"]=4 ["vgg19"]=4)

for net in ${network_list[@]}; do
    echo ${net}
    echo ${batchsize_lineno_map[${net}]}
done

