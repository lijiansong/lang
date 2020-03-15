#!/bin/bash
perf stat -e imc/cas_count_read/,imc/cas_count_write/ caffe test --weights ssd_mobilenetv1/ssd_mobilenetv1_float16_dense.caffemodel --model ssd_mobilenetv1/ssd_mobilenetv1_float16_dense_1batch.prototxt --iterations 4
