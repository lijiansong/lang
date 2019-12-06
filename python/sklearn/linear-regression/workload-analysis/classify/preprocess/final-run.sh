#!/bin/bash
# --------------------------------------------------------
# Notice: please make sure install timing tool, bc
# Otherwise you will fail to execute this script!
# --------------------------------------------------------

current_dir=`pwd`
exe=${current_dir}/../../build/examples/clas_offline_multicore/clas_offline_multicore

#${exe} -offlinemodel ${current_dir}/offline.cambricon -images ${current_dir}/file_list_for_release -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline.cambricon -images ${current_dir}/file_list_for_cifar10 -labels ${current_dir}/labels.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-alexnet-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-mobilenet-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-resnet101-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-squeezenet-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-inception-v3-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-resnet152-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-resnet18-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-resnet34-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-resnet50-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-vgg19-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-vgg16-int8.cambricon -images ${current_dir}/val-5w.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 4 -dataparallel 8 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4

#${exe} -offlinemodel ${current_dir}/offline-mobilenet/offline-mobilenet-float16-dense-256batch-1.cambricon -images ${current_dir}/val-2k.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 16 -dataparallel 32 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
#${exe} -offlinemodel ${current_dir}/offline-mobilenet/offline-mobilenet-float16-dense-256batch-1.cambricon -images ${current_dir}/val-2k.txt -labels ${current_dir}/synset_words.txt -int8 1  -fifosize 2  -threads 16 -dataparallel 32 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4

#${exe} -offlinemodel ${current_dir}/offline-densenet121/offline-densenet121-float16-dense-4batch-1.cambricon -images ${current_dir}/val-5k.txt -labels ${current_dir}/synset_words.txt -int8 0  -fifosize 2  -threads 8 -dataparallel 4 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
${exe} -offlinemodel ${current_dir}/offline-resnet50/offline-resnet50-float16-dense-4batch-1.cambricon -images ${current_dir}/val-5k.txt -labels ${current_dir}/synset_words.txt -int8 0  -fifosize 2  -threads 8 -dataparallel 4 #&>> ${current_dir}/val.log-int8-dense-8batch-8-1-4
