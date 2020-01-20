#!/bin/bash

CNRT_ERR_DIR_NAME=cnrt-error
LOG_PREFIX=resnet50.log-int8-dense-*

if [ ! -d ${CNRT_ERR_DIR_NAME} ]
then
    mkdir ${CNRT_ERR_DIR_NAME}
fi

grep -ril "cnrtError" ${LOG_PREFIX} | xargs -i mv {} ${CNRT_ERR_DIR_NAME}

grep -rin "End2end throughput fps" ${LOG_PREFIX} 2>&1 | tee end2end-fps.log
grep -rin "Hardware fps" ${LOG_PREFIX} 2>&1 | tee hardware-fps.log
grep -rin "Total execution time" ${LOG_PREFIX} 2>&1 | tee total-exe-time.log
grep -rin "Global accuracy" ${LOG_PREFIX} | cut -d ":" -f1,2 2>&1 | tee acc.log
python3 extract_acc.py acc.log
mv end2end-fps.log hardware-fps.log total-exe-time.log scripts

grep -rin "prepare input data" ${LOG_PREFIX} 2>&1 | tee prepare-input.log
grep -rin "copyin time" ${LOG_PREFIX} 2>&1 | tee copyin-time.log
grep -rin "execution time" ${LOG_PREFIX} 2>&1 | tee execution-time.log
grep -rin "copyout time" ${LOG_PREFIX} 2>&1 | tee copyout-time.log
grep -rin "post process time" ${LOG_PREFIX} 2>&1 | tee post-process-time.log
mv prepare-input.log copyin-time.log execution-time.log copyout-time.log post-process-time.log scripts
