#!/bin/bash
# Note: shell has no built-in map data structure

declare line_map=(["100"]=1 ["200"]=2)
line_map["300"]="3"

echo ${line_map[@]}

# iterator
for key in ${!line_map[@]};
do
    echo ${key}
    echo ${line_map[${key}]}
done

batchsize_lineno_map=(
"alexnet|4"
"googlenet|4"
"inception-v3|8"
"mobilenet|8"
"resnet101|4"
"resnet152|4"
"resnet18|4"
"resnet34|4"
"resnet50|4"
"squeezenet|11"
"vgg16|4"
"vgg19|4"
)

for item in ${batchsize_lineno_map[@]}; do
    net=$(echo "${item}"|awk -F "|" '{print $1}')
    line_no=$(echo "${item}"|awk -F "|" '{print $2}')
    echo "net: ${net}, line_no: ${line_no}"
done

