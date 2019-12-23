#!/bin/bash
caffe test -iterations 5000 -mmode MLU -mludevice 0 -mcore MLU100 -model DenseNet_121-online.prototxt -weights DenseNet_121.caffemodel 2>&1 | tee mlu-densenet-121.log
#caffe test -iterations 5000 -mmode MLU -mludevice 0 -mcore MLU100 -model DenseNet_161-online.prototxt -weights DenseNet_161.caffemodel 2>&1 | tee mlu-densenet-161.log
#caffe test -iterations 5000 -mmode MLU -mludevice 0 -mcore MLU100 -model DenseNet_169-online.prototxt -weights DenseNet_169.caffemodel 2>&1 | tee mlu-densenet-169.log
#caffe test -iterations 5000 -mmode MLU -mludevice 0 -mcore MLU100 -model DenseNet_201-online.prototxt -weights DenseNet_201.caffemodel 2>&1 | tee mlu-densenet-201.log
#caffe test -iterations 5000 -mmode MFUS -mludevice 0 -mcore MLU100 -model DenseNet_201-online.prototxt -weights DenseNet_201.caffemodel 2>&1 | tee mlu-fuse-densenet-201.log
